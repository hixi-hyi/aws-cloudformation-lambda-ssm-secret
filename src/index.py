from cfnprovider import CustomResourceProvider, get_logger
import boto3
import os
import string
import secrets
logger = get_logger(__name__)
env = os.environ

class Secret(CustomResourceProvider):
  def init(self):
    self._name = self.get('Name')
    self._pattern = self.get('Pattern', string.ascii_letters + string.digits)
    self._length = int(self.get('Length', 32))

    self._ssm = boto3.client('ssm')
    self.response.physical_resource_id = self.id
    self.response.set_data('Name', self._name)

  @property
  def id(self):
    return "{}".format(self._name)

  def generate(self):
    secret = ''.join(secrets.choice(self._pattern) for _ in range(self._length))
    return secret

  def set_secret(self, secret):
    self.response.set_data('Secret', secret)

  def put_ssm(self, secret, overwrite=False):
    self._ssm.put_parameter(
      Name=self._name,
      Value=secret,
      Type="SecureString",
      Overwrite=overwrite,
    )

  def get_ssm(self):
    secret = self._ssm.get_parameter(
      Name=self._name,
      WithDecryption=True
    )['Parameter']['Value']
    return secret

  def process_new_secret(self, overwrite=False):
    secret = self.generate()
    self.put_ssm(secret, overwrite)
    self.set_secret(secret)
    return

  def create(self, policies):
    if policies.has('UseIfExists'):
      # For define the infrastructure already created
      secret = self.get_ssm()
      if secret:
        self.set_secret(secret)
        return
    elif policies.has('Overwrite'):
      self.process_new_secret(overwrite=True)
      return

    self.process_new_secret(overwrite=False)

  def update(self, policies):
    if policies.has('Retain'):
      # For safety
      secret = self.get_ssm()
      if not secret:
        raise 'Do not have secret'
      self.set_secret(secret)
      return

    self.process_new_secret(overwrite=True)

  def delete(self, policies):
    if policies.has('Retain'):
      return

    try:
      self._ssm.delete_parameter(Name=self._name)
    except Exception as e:
      if policies.has('IgnoreError'):
        return
      raise e

def handler(event, context):
  c = Secret(event, context)
  c.handle()

