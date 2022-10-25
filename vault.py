import logging
import logging.config
import os
from pprint import pprint

import hvac

from produce_pwds import Password

logging.config.fileConfig(fname="onlogs.conf", disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger("avamar_automation")


class Vault(object):
    def __init__(
        self, url="https://vault-acs-prod.amer.thermo.com", username=None, password=None
    ):
        self.client = hvac.Client(url=url)

        self.username = os.getenv("VAULT_USERNAME", username)
        self.password = os.getenv("VAULT_PASSWORD", password)

        self.client.auth.ldap.login(username=self.username, password=self.password)

        if self.client.is_authenticated():
            logger.info(" Successfully connected to vault ...")
        else:
            logger.exception(" Failed to connect to vault ...")
            raise

    def create_or_update_server(self, server_name, admin, dpn, root):
        secret_path = "avamar/servers/" + server_name
        self.client.secrets.kv.v1.create_or_update_secret(
            path=secret_path, secret={"admin": admin, "dpn": dpn, "root": root}
        )
        logger.info(f"\n\n Successfully created/updated secret for '{server_name}'\n\n")

    def read_secret(self, path):
        return self.client.secrets.kv.v1.read_secret(path=path)["data"]

    def delete_server(self, server_name):
        secret_path = "avamar/servers/" + server_name
        self.client.secrets.kv.v1.delete_secret(path=secret_path)
        logger.info(" Secret '%s' was deleted from vault ...", server_name)
        return self.list_servers()

    def read_server(self, server_name):
        secret_path = "avamar/servers/" + server_name
        read_secret_result = self.client.secrets.kv.v1.read_secret(
            path=secret_path
        )  # raises an exception if path is invalid

        return read_secret_result["data"]

    def list_servers(self):
        list_secrets_result = self.client.secrets.kv.v1.list_secrets(
            path="avamar/servers/"
        )
        return list_secrets_result["data"]["keys"]

    def print_secret(self, server_name):
        """For debugging purposes"""
        secret_path = "avamar/servers/" + server_name
        read_secret_result = self.client.secrets.kv.v1.read_secret(path=secret_path)
        credentials = read_secret_result["data"]

        logger.debug(f"\n --- SECRET FOR: '{server_name}' ---")
        logger.debug("root: '%s'", credentials["root"])
        logger.debug("dpn: '%s'", credentials["dpn"])
        logger.debug("admin: '%s'", credentials["admin"])


# if __name__ == "__main__":
#     pw = Password()
#     store = Vault(username="amer.svc.ansible", password="gsV65Tf7")

#     information = store.create_or_update_server(
#         server_name="brz-avmrn1-01.amer.thermo.com",
#         admin=pw.read_passwords("admin"),
#         dpn=pw.read_passwords("dpn"),
#         root=pw.read_passwords("root"),
#     )

#     # logger.info(f"\n\nstore.print_secret({server_name})")
#     # store.print_secret(server_name)
