from azuresearch.base_api_call import BaseApiCall


class Indexer(BaseApiCall):


    def __init__(self, name, data_source_name, target_index_name, skillset_name, field_mappings=None,
                 output_field_mappings=None, schedule=None, disabled=False, parameters=None, **params):
        super(Indexer, self).__init__(service_name = "indexer")
        self.output_field_mappings = output_field_mappings
        self.field_mappings = field_mappings
        self.skill_set_name = skillset_name
        self.target_index_name = target_index_name
        self.data_source_name = data_source_name
        self.name = name
        self.schedule = schedule
        self.disabled = disabled

        if self.field_mappings is None:
            self.field_mappings = []
        if self.output_field_mappings is None:
            self.output_field_mappings = []

        if params:
            self.params = params['kwargs']
        else:
            self.params = {}

    def __repr__(self):
        return "<Indexer: \n" \
               "indexer name: {name}\n, " \
               "data_source_name: {data_source_name}\n" \
               "target_index_name: {target_index_name}\n" \
               "skillset_name: {skillset_name}\n" \
               "field_mappings: {field_mappings}\n" \
               "output_field_mappings: {output_field_mappings}".format(name=self.name,
                                                                       data_source_name=self.data_source_name,
                                                                       target_index_name=self.target_index_name,
                                                                       skillset_name=self.skill_set_name,
                                                                       field_mappings=self.field_mappings,
                                                                       output_field_mappings=self.output_field_mappings)

    def to_dict(self):
        dict = {
            "name": self.name,
            "dataSourceName": self.data_source_name,
            "targetIndexName": self.target_index_name,
            "skillsetName": self.skillset_name,
            "fieldMappings": [fm.to_dict() for fm in self.field_mappings],
            "outputFieldMappings": [fm.to_dict() for fm in self.output_field_mappings],
            "schedule": self.schedule,
            "disabled": self.disabled,
            "parameters": self.parameters
        }

        # Add additional arguments
        dict.update(self.params)

        # Remove None values
        dict = {k: v for k, v in dict.items() if v is not None}
        return dict


class IndexerSchedule(object):
    def __init__(self, interval, start_time=None):
        """
    :param interval: Required. A duration value that specifies an interval or period for indexer runs. The smallest allowed interval is five minutes; the longest is one day. It must be formatted as an XSD "dayTimeDuration" value (a restricted subset of an ISO 8601 duration value). The pattern for this is: "P[nD][T[nH][nM]]". Examples: PT15M for every 15 minutes, PT2H for every 2 hours.
    :param start_time: Optional. A UTC datetime when the indexer should start running.
       """
        self.interval = interval
        self.start_time = start_time

    def to_dict(self):
        return {"interval": self.interval,
                "startTime": self.start_time}
