import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from settings import CREDENTIALS_FILE
import httplib2

# регистрация и получение экземпляра доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)
