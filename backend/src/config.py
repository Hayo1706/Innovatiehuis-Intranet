# IF TRUE, JWT VERIFICATION AND PERMISSION CHECKING ARE DISABLED (ALLOWS USE OF SWAGGER UI TO TEST ENDPOINTS)
DEBUG_MODE = False

# IF TRUE, TWO FACTOR AUTHENTICATION IS REQUIRED AT LOGIN
TWO_FACTOR = False

# ROOT DIRECTORY FOR ALL DATA FILES - MUST ALWAYS END IN A '/'!
FILE_STORAGE_ROOT = '../filestorage/root/'

DATABASE_URL = 'mariadb+mariadbconnector://root:admin@127.0.0.1:3306/innovatieplatform'

JWT_ISSUER = 'innovatieplatform'
JWT_SECRET = 'kiZn04wb0XEPfpnkTbgmFtHtNElRThM2nWNdD51KaosfRT8HzVLqPB3UMnKPwb1'  # TODO Change This? Moet Secret om de zo veel tijd gerefreshed worden?
JWT_LIFETIME_SECONDS = 2400     # USERS WILL BE REQUIRED TO RE-AUTHENTICATE (LOGIN) AFTER THIS NUMBER OF SECONDS
JWT_REFRESH_TIME_SECONDS = JWT_LIFETIME_SECONDS/4
JWT_ALGORITHM = 'HS256'

# COOLDOWN WILL START AFTER THIS NUMBER OF FAILED LOGIN ATTEMPTS
ATTEMPTS_BEFORE_COOLDOWN = 6
# DURING COOLDOWN, THE API WILL IGNORE ANY LOGIN ATTEMPTS
COOLDOWN_TIME_SECONDS = 10

# OLDER ANNOUNCEMENTS WILL NOT BE RETURNED BY THE API (0 MEANS ALL ANNOUNCEMENTS WILL BE RETURNED)
# TODO: NOT YET IMPLEMENTED!
CUTOFF_DATE = 0

MAX_PASSWORD_LENGTH = 20
MIN_PASSWORD_LENGTH = 3
FORCE_SPECIAL_CHARACTER = True
FORCE_NUMBERS = True
FORCE_CAPITAL_LETTERS = True

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'innovatiehuis.platform@gmail.com'
MAIL_PASSWORD = '2SvNyLGPqeEkJ57'
MAIL_USE_TLS = False
MAIL_USE_SSL = True



MAX_NAME_LENGTH = 36            # AMOUNT OF SAFE CHARS ALLOWED IN FOLDER AND FILE NAMES
ALLOWED_FILE_TYPES = ['jpg', 'jpeg', 'png', 'pdf', 'docx', 'csv', 'xlsx', 'pptx', 'txt', 'json']  #HAS TO BE CONNECTED TO FRONTEND
MAX_FILE_SIZE = 100000000       # AMOUNT OF BYTES ALLOWED PER FILE

PASSWORD_CHANGE_SECRET_KEY = "{sPnF[{/Zn-U,&{3KsW\dk*+L%}M'/NW"
DOMAIN_NAME = 'http://localhost:8080'