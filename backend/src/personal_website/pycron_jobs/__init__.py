from personal_website.core.utils import PyCronJob, get_all_subclasses
from personal_website.pycron_jobs import send_tg_messages

pycron_jobs = {cls.__name__: cls for cls in get_all_subclasses(PyCronJob)}
