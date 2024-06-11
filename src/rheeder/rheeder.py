"""Main module."""
import base64
import os


class ReaderImp:
    """
    Interface for all ReaderImp concrete classes.
    """

    def read(self, path) -> str:
        """
        Read from path and return contents

        Args:
            path: path/to/read/from
        """
        raise NotImplementedError


class LocalReaderImp(ReaderImp):
    """
    Read from a local directory.
    """

    def __init__(self, path_prefix: str):
        """
        Args:
            path_prefix: path/to/directory to read from
        Example:
            import os
            import rheeder

            reader = rheeder.LocalReaderImp(
                path_prefix=os.path.dirname(__file__)
            )

        """
        self.path_prefix = path_prefix

    def read(self, path: str) -> str:
        with open(os.path.join(self.path_prefix, path), encoding="utf-8") as f:
            contents = f.read()
        return contents


class S3ReaderImp(ReaderImp):
    """
    Read from S3.
    """

    def __init__(self, boto3_client: str, bucket: str):
        """
        Args:
            boto3_client =. bot03.client
            bucket: s3 bucket
        Example:
            import boto3
            import rheeder

            reader = rheeder.S3ReaderImp(
                boto3_client=boto3.client('s3'),
                bucket='my-bucket'
            )
        """
        self.client = boto3_client
        self.bucket = bucket

    def read(self, path: str) -> str:
        response = self.client.get_object(Bucket=self.bucket, Key=path)
        return response["Body"].read()


class GithubGetContentsReaderImp(ReaderImp):
    """
    Read from a Github repo by fetching file contents per file.
    """

    def __init__(self, pygithub_repo: "github.Repository.Repository"): # noqa: F821
        """
        Args:
            pygithub_repo:
              See https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html
        Example:
            import github
            import rheeder

            auth = github.Auth.Token("access_token")
            g = github.Github(auth=auth)
            repo = g.get_repo("PyGithub/PyGithub")

            reader = rheeder.GithubGetContentsReaderImp(
                pygithub_repo=repo
            )
        """
        self.repo = pygithub_repo

    def read(self, path: str) -> str:
        content_file = self.repo.get_contents(path)
        return base64.b64decode(content_file.content)


class GithubCloneRepoReaderImp(ReaderImp):
    """
    Read from a Github repo using an initial clone of the repo.
    """

    def __init__(self, gitpython_repo: "git.Repo"): # noqa: F821
        """
        Args:
            repo:
              Example:
                from git import Repo
                import rheeder

                repo = Repo.clone_from(repo_url, local_dir)

                reader = rheeder.GithubCloneRepoReaderImp(
                    gitpython_repo=repo
                )
        Ref:
        - https://gitpython.readthedocs.io/en/stable/quickstart.html
        """
        self.repo = gitpython_repo

    def read(self, path: str) -> str:
        # TODO:
        with os.path.join(self.repo.working_tree_dir, path, encoding="utf-8") as f:
            contents = f.read()
        return contents


class TransparentReaderImp(ReaderImp):
    """
    Read contents by directly passing them through the read method.
    """

    def read(self, path: str) -> str:
        """
        Args:
            path: contents are returned as-is
        """
        return path
