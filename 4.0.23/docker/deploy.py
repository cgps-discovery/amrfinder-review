import subprocess
import argparse
import logging
import zipfile
import os
import urllib.request
import shutil
import os
import re
import tarfile
import json

def build(args):

    logging.info("Building Docker image")
    logging.info(f"Arguments: {args}")
    
    docker_build(args.docker_dir, args.docker_repo, args.docker_image_version, args.image_target, args.push)

def test(args):
    logging.info("Testing Docker image")
    logging.info(f"Arguments: {args}")    

    test_docker_run(args.docker_repo + ':' + args.docker_image_version + f"-{args.image_target}", args.test_dir)

def describe(args):
    arg_versions, labels, python_requirements = docker_describe(args.docker_dir)
    for label in labels:
        value = label.split('=')[1].replace('"', '').strip()
        print(f"* {label.title().split('=')[0].replace('.', ' ')}: {value}")
    if arg_versions:
        print("\n## Sofware versions:\n")
        for arg in arg_versions:
            print(f"\t* {arg[0].title().split('_')[0]}: {arg[1]}")
    if python_requirements:
        print(f"\n## Python requirements:\n")
        for key, value in python_requirements.items():
            print(f"\t* {key}: {value}")

def docker_describe(docker_dir):
    dockerfile_path = f'{docker_dir}/Dockerfile'
    with open(dockerfile_path, 'r') as file:
        data = file.read()

        # Extract ARG software versions
        arg_versions = re.findall(r'ARG\s+(\w+)\s*=\s*(.*)', data)

        # Extract LABEL information
        labels = re.findall(r'LABEL\s+(.*?)\s*$', data, re.MULTILINE)

        # Extract Python requirements
        python_requirements = {} 
        python_requirements_matches = re.findall(r'RUN\s+pip[3]*\s+install [--no\-cache\-dir]*\s+(.*==.+)', data)
        for match in python_requirements_matches:
            python_requirements.update({x.split("==")[0]:x.split("==")[1] for x in match.split() })
        return arg_versions, labels, python_requirements



def docker_build(docker_dir, docker_repo, docker_image_version, image_type='aws', push=False):
    """
    Build and compile a Docker image.

    Args:
        docker_dir (str): The directory containing the Dockerfile.
        docker_repo (str): The name of the Docker repository.
        docker_image_version (str): The version of the Docker image.
        image_type (str, optional): The type of image to build. Defaults to 'aws'.
        push (bool, optional): Whether to push the built image to the repository. Defaults to False.
    """
    image_cache = f'{docker_repo}:{docker_image_version}-{image_type}'
    os.environ["DOCKER_BUILDKIT"] = "1"
    cmd = ['docker', 'build', '--target', image_type, '--build-arg', 'BUILDKIT_INLINE_CACHE=1', f'--cache-from={image_cache}', '--tag', image_cache, docker_dir]
    logging.info(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    if push:
        cmd = ['docker', 'push', image_cache]
        logging.info(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)


def amrfinder_test_1(docker_image, test_dir_abs):
    """
    Run dataset 1 using the specified Docker image and test directory.

    Args:
        docker_image (str): The Docker image to use for running the tests.
        test_dir_abs (str): The absolute path of the test directory.

    Raises:
        AssertionError: If any of the required output files do not exist or have a size of 0.
    """
    logging.info('Running AMRFinder dataset 1 via Docker')

    # Build docker run command to accept stdin FASTA and pass args to amrfinder
    docker_cmd = [
        'docker', 'run', '--rm', '-i', docker_image,
        '--tax-id', '1313'
    ]

    fasta_path = os.path.join(test_dir_abs, 'testing_basic', 'ERR054556.fasta')
    if not os.path.exists(fasta_path):
        raise FileNotFoundError(f"Test FASTA not found: {fasta_path}")

    # Run the container and pipe the FASTA into stdin
    with open(fasta_path, 'rb') as fasta_file:
        result = subprocess.run(docker_cmd, stdin=fasta_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        logging.error('Docker run failed')
        logging.error(result.stderr.decode('utf-8'))
        raise RuntimeError(f'Docker run returned non-zero exit code: {result.returncode}')

    output = result.stdout.decode('utf-8').strip()
    if not output:
        output = result.stderr.decode('utf-8').strip()

    try:
        parsed = json.loads(output)
    except Exception as e:
        logging.error("Expected JSON output from container but failed to parse.")
        logging.error("Container output:\n" + output)
        raise AssertionError(f"Output is not valid JSON: {e}")

    if not isinstance(parsed, (dict, list)):
        raise AssertionError("JSON output is not an object or array")

    # Emit normalized JSON to stdout
    print(json.dumps(parsed))
  

def test_docker_run(docker_image, test_dir="test/"):
    """
    Run tests for a Docker image by executing it with the specified image and test directory.

    Args:
        docker_image (str): The Docker image to test.
        test_dir (str, optional): The directory containing the test data. Defaults to "test/".

    Raises:
        AssertionError: If the Docker run fails or the output is unexpected.

    """
    # Check basic help/usage output from the image's run.py
    result = subprocess.run(['docker', 'run', '--rm', docker_image, '-h'], capture_output=True, text=True)
    out = (result.stdout or result.stderr or "").lower()
    assert 'usage:' in out and '--tax-id' in out, f"Docker run failed to show expected usage/help; output:\n{result.stdout}\n{result.stderr}"

    test_dir_abs = os.path.abspath(test_dir)

    # Run a genome
    logging.info(f"Running test with {docker_image} and {test_dir}")

    amrfinder_test_1(docker_image, test_dir_abs)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Deploy EToKi Docker images.')
    # aws repo = 902121496535.dkr.ecr.us-east-2.amazonaws.com/cgps-discovery
    parser.add_argument('--docker-dir', help='Directory containing Dockerfile', default="4.0.23/docker")
    parser.add_argument('--docker-repo', help='Docker repository name', default="happykhan/amrfinder")
    parser.add_argument('--docker-image-version', help='Docker image version', default="amrfinder-latest")

    subparsers = parser.add_subparsers(dest='command')

    build_parser = subparsers.add_parser('build', help='Build Docker images')
    build_parser.set_defaults(func=build)
    build_parser.add_argument('--push', help='Push to remote (dockerhub or aws depending on docker-repo)', default=False, action='store_true')
    build_parser.add_argument('--image-target', help='Docker image target', choices=['base', 'runtime', 'nextflow'], default='runtime')
    build_parser.add_argument('--docker-dir', help='Directory containing Dockerfile', default="4.0.23/docker")
    build_parser.add_argument('--docker-repo', help='Docker repository name', default="happykhan/amrfinder")
    build_parser.add_argument('--docker-image-version', help='Docker image version', default="amrfinder-latest")

    test_parser = subparsers.add_parser('test', help='Test Docker images with sample data')
    test_parser.add_argument('--test-dir', help='Directory of test data', default="./")
    test_parser.add_argument('--image-target', help='Docker image target', choices=['base', 'runtime', 'nextflow'], default='runtime')
    test_parser.add_argument('--delete-test-on-sucess', help='Delete directory on success', default=False, action='store_true')
    test_parser.set_defaults(func=test)

    describe_parser = subparsers.add_parser('describe', help='Describe Docker images')
    describe_parser.add_argument('--docker-dir', help='Directory containing Dockerfile', default="4.0.23/docker")
    describe_parser.set_defaults(func=describe)

    args = parser.parse_args()
    args.func(args)

