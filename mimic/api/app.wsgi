from mimic.common import service
from mimic.api import app


service.prepare_service([])

application = app.VersionSelectorApplication() 
