class OpenAI:
    API_TYPE = "azure"
    API_BASE = "https://eastus.api.cognitive.microsoft.com/"
    API_VERSION= "2023-03-15-preview"
    API_KEY = "51a522a1f13247918514f9c14b196625"
    MODEL = "Eximius-Resume"
    MODEL_JD = "eximius-davinci"
    MODEL_NAME = "exim-embedd" # "exim-embedding" #Vector Search



class Cosmos:
    URL = "https://eximiuscosmo.documents.azure.com:443/"
    KEY = "h6us8ihYGQd1xB5RDF0NQQJEMhgg3Z1q8U8VgYJgnahaADJ5oyb9OFCopGAYf5tRq0uYIp6RgSrrACDbDCpAZA=="
    DATABASE_NAME = 'eximiusCosmosDb'
    CONTAINER_NAME_RESUME = 'Resume'
    CONTAINER_NAME_JD = 'Job'

