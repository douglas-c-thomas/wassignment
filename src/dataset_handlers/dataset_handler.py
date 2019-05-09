from google.cloud import bigquery


class DatasetHandler(object):
    """
    The DatasetHandler is an abstract class that defines how dataset handlers should behave.  Each dataset handler
    subclass should know how to properly execute a query against a given dataset, as well as how to persist the
    result sets for future inspection.
    """
    def __init__(self):
        self.client = bigquery.Client()

    @classmethod
    def get_class_for_dataset(cls, dataset_name):
        """
        Getting the class name could probably be done a little more cleanly, but converting:
            "unemployment_cps" to "UnemploymentCPSDatasetHandler"
        by changing case in a weird way and dropping underscores seems like technical debt we can keep at the moment

        :param dataset_name: The name of the dataset
        :return: The name of the dataset handler that will act appropriately
        """
        mapping = {
            'unemployment_cps': 'UnemploymentCPSDatasetHandler'
        }
        return mapping.get(dataset_name)

    def execute_query(self, dataset, query, limit):
        """
        The execute_query function implements the query execution against a particular BLS dataset

        :param dataset: The dataset in question
        :param query:  The query parameters to send to the Google Big Query engine
        :param limit: The maximum number of records to return
        :return: A Big Query Result Set
        """
        raise NotImplementedError('Subclasses should implement the query execution implementation')
