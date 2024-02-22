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
    cmd = ['docker', 'build', '--target', image_type, '--build-arg', 'BUILDKIT_INLINE_CACHE=1', f'--cache-from={image_cache}', '--tag', image_cache, docker_dir]
    logging.info(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    if push:
        cmd = ['docker', 'push', image_cache]
        logging.info(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

def fetch_test_data(test_dir="test/"):
    """
    Fetches test data from a specified URL and extracts it to the given directory.

    Args:
        test_dir (str): The directory where the test data will be extracted. Defaults to "test/".

    Returns:
        None
    """
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    url = "https://zenodo.org/records/5704419/files/reads.zip?download=1"
    logging.info(f"Fetching test data from {url}")
    if not os.path.exists(test_dir +'/illumina/T4_R1.fastq.gz') or not os.path.exists(test_dir +'/illumina/T7_R1.fastq.gz'):
        file_name = f'{test_dir}/reads.zip' 
        urllib.request.urlretrieve(url, file_name)
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(test_dir)
        os.remove(file_name)
        logging.info(f"Etoki test data extracted to {test_dir}")

    if not os.path.exists(test_dir +'/test_samples/SRX5084910_SRR8268082_R1.fastq.gz') or not os.path.exists(test_dir +'/test_samples/SRX5084941_SRR8268051_R1.fastq.gz'):
        url = "https://figshare.com/ndownloader/files/41228577"
        logging.info(f"Fetching test data from {url}")
        file_name = f'{test_dir}/test_samples.tar.gz'
        urllib.request.urlretrieve(url,file_name)
        with tarfile.open(file_name, 'r:gz') as tar_ref:
            tar_ref.extractall(test_dir)
        os.remove(file_name)
        logging.info(f"Confinder test data extracted to {test_dir}")
    # test 3 
    test_3 = ["ftp.sra.ebi.ac.uk/vol1/fastq/SRR274/061/SRR27410861/SRR27410861_1.fastq.gz", 
              "ftp.sra.ebi.ac.uk/vol1/fastq/SRR274/061/SRR27410861/SRR27410861_2.fastq.gz", 
              "ftp.sra.ebi.ac.uk/vol1/fastq/ERR586/ERR586796/ERR586796_1.fastq.gz", 
              "ftp.sra.ebi.ac.uk/vol1/fastq/ERR586/ERR586796/ERR586796_2.fastq.gz"]
    test_3_dir = os.path.join(test_dir, "test_3")
    if not os.path.exists(test_3_dir):
        os.makedirs(test_3_dir)        
    for fastq in test_3:    
        file_name = f'{test_3_dir}/{fastq.split("/")[-1]}'        
        if not os.path.exists(file_name):
            logging.info(f"Fetching test data from {fastq}")
            urllib.request.urlretrieve(f"ftp://{fastq}", file_name)
            logging.info(f"Downloaded {file_name}")


def amrfinder_test_1(docker_image, test_dir_abs):
    """
    Run dataset 1 using the specified Docker image and test directory.

    Args:
        docker_image (str): The Docker image to use for running the tests.
        test_dir_abs (str): The absolute path of the test directory.

    Raises:
        AssertionError: If any of the required output files do not exist or have a size of 0.
    """
    logging.info('Running dataset 1')
    
    result = subprocess.run(['docker', 'run', '--platform=linux/x86_64', '--rm', '-v', f'{test_dir_abs}/illumina:/data', docker_image, 'EToKi.py', 'prepare', '--pe', '/data/T7_R1.fastq.gz,/data/T7_R2.fastq.gz', '-p', '/data/prep_out'])
    result = subprocess.run(['docker', 'run', '--platform=linux/x86_64', '--rm', '-v', f'{test_dir_abs}/illumina:/data', docker_image, 'EToKi.py', 'assemble', '--pe', '/data/prep_out_L1_R1.fastq.gz,/data/prep_out_L1_R2.fastq.gz', '-p', '/data/asm_out'])

    # Check if the output file exists and has a size larger than 0
    required_output_files = [f'{test_dir_abs}/illumina/asm_out.result.fasta', f'{test_dir_abs}/illumina/asm_out.result.fastq' ] 
    for required in required_output_files: 
        assert os.path.exists(required) and os.path.getsize(required) > 0, f"Output file {required} does not exist or has a size of 0"
  

def test_docker_run(docker_image, test_dir="test/"):
    """
    Run tests for a Docker image by executing it with the specified image and test directory.

    Args:
        docker_image (str): The Docker image to test.
        test_dir (str, optional): The directory containing the test data. Defaults to "test/".

    Raises:
        AssertionError: If the Docker run fails or the output is unexpected.

    """
    # Check basic --help output 
    result = subprocess.run(['docker', 'run',  '--platform=linux/x86_64', docker_image, 'amrfinder'], capture_output=True)
    assert result.stdout.decode('utf-8').splitlines()[0] == 'usage: EToKi [-h]', f"Docker run failed, Unexpected output: {result.stdout.decode()}"

    test_dir_abs = os.path.abspath(test_dir)

    # Run a small dataset
    # fetch_test_data(test_dir)
    # logging.info(f"Running test with {docker_image} and {test_dir}")

    # amrfinder_test_1(docker_image, test_dir_abs)

    # Delete test directory on success
    if args.delete_test_on_sucess:
        shutil.rmtree(args.test_dir)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Deploy EToKi Docker images.')
    # aws repo = 902121496535.dkr.ecr.us-east-2.amazonaws.com/cgps-discovery
    parser.add_argument('--docker-dir', help='Directory containing Dockerfile', default="3.12.8/docker")
    parser.add_argument('--docker-repo', help='Docker repository name', default="happykhan/amrfinder")
    parser.add_argument('--docker-image-version', help='Docker image version', default="amrfinder-latest")
    parser.add_argument('--image-target', help='Docker image target', choices=['base', 'aws', 'runtime'], default='aws')

    subparsers = parser.add_subparsers(dest='command')

    build_parser = subparsers.add_parser('build', help='Build Docker images')
    build_parser.set_defaults(func=build)
    build_parser.add_argument('--push', help='Push to remote (dockerhub or aws depending on docker-repo)', default=False, action='store_true')

    test_parser = subparsers.add_parser('test', help='Test Docker images with sample data')
    test_parser.add_argument('--test-dir', help='Directory to run tests', default="test/")
    test_parser.add_argument('--delete-test-on-sucess', help='Delete directory on success', default=False, action='store_true')
    test_parser.set_defaults(func=test)

    describe_parser = subparsers.add_parser('describe', help='Describe Docker images')
    describe_parser.add_argument('--docker-dir', help='Directory containing Dockerfile', default="docker")
    describe_parser.set_defaults(func=describe)

    args = parser.parse_args()
    args.func(args)

