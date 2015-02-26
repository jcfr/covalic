import os
import re
import requests
import shutil
import subprocess
import zipfile


def _readFilenameFromResponse(request):
    """
    This helper will derive a filename from the HTTP response, first attempting
    to use the content disposition header, otherwise falling back to the last
    token of the URL.
    """
    match = re.search('filename="(.*)"', request.headers['Content-Disposition'])

    if match is None:
        return [t for t in request.url.split('/') if t][-1]
    else:
        return match.group(1)


def pullDockerImage(image):
    """
    Pulls the docker image to the local system by calling "docker pull <image>".
    If the pull fails, this raises an exception.
    """
    command = ('docker', 'pull', image)
    p = subprocess.Popen(args=command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    if p.returncode != 0:
        print('Error pulling docker image %s:' % image)
        print('STDOUT: ' + stdout)
        print('STDERR: ' + stderr)

        raise Exception('Docker pull returned code {}'.format(p.returncode))


def fetchHttpInput(tmpDir, spec):
    """
    Downloads an input file via HTTP using requests.
    """
    if 'url' not in spec:
        raise Exception('No URL specified for HTTP input.')

    request = requests.get(spec['url'], headers=spec.get('headers', {}))
    try:
        request.raise_for_status()
    except:
        print 'HTTP fetch failed (%s). Response: %s' % \
            (spec['url'], request.text)
        raise

    filename = spec.get('filename', _readFilenameFromResponse(request))
    path = os.path.join(tmpDir, filename)

    total = 0
    maxSize = spec.get('maxSize')

    with open(path, 'wb') as out:
        for buf in request.iter_content(32768):
            length = len(buf)
            if maxSize and length + total > maxSize:
                raise Exception('Exceeded max download size of {} bytes.'
                                .format(maxSize))
            out.write(buf)
            total += length

    return path


def fetchInputs(tmpDir, inputList):
    """
    Fetch all inputs. For each input, writes a '_localPath' key into the
    input spec that denotes where the file was written on the local disk.
    """
    localFiles = {}

    for label, input in inputList.iteritems():
        inputType = input.get('type', 'http').lower()

        if inputType == 'http':
            localFiles[label] = fetchHttpInput(tmpDir, input)
        else:
            raise Exception('Invalid input type: ' + inputType)

    return localFiles


def cleanup(tmpDir):
    """
    Cleanup from a job is performed by this function. For now, this is simply
    deleting the temp directory.

    :param tmpDir: The temporary directory to remove.
    """
    if os.path.isdir(tmpDir):
        shutil.rmtree(tmpDir)


def extractZip(path, dest, flatten=False):
    """
    Extract a zip file, optionally flattening it into a single directory.
    """
    try:
        os.makedirs(dest)
    except OSError:
        if not os.path.exists(dest):
            raise

    with zipfile.ZipFile(path) as zf:
        if flatten:
            for name in zf.namelist():
                out = os.path.join(dest, os.path.basename(name))
                with open(out, 'wb') as ofh:
                    with zf.open(name) as ifh:
                        while True:
                            buf = ifh.read(65536)
                            if buf:
                                ofh.write(buf)
                            else:
                                break
        else:
            zf.extractall(output)
