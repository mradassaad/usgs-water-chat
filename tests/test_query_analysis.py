import unittest
import query_analysis

class TestQueryAnalysis(unittest.TestCase):

    def test_get_and_filter_str(self):
        # Create a ThingsSearchModel instance
        search_params = query_analysis.ThingsSearchModel(
                state='CA',
                county='Los Angeles',
                active=True,
                monitoring_location_type='Stream',
                observed_property='Discharge')
            
        # Create a ThingsSearchUrl instance
        search_url = query_analysis.ThingsSearchUrl(search_params)

        # Construct the URL with the get_and_filter_str method
        result = search_url.get_and_filter_str()
        
        # Check the result
        expected_url = "(properties/state eq 'CA' and properties/county eq 'Los Angeles' and properties/active eq True and properties/monitoringLocationType eq 'Stream')"
        self.assertEqual(result, expected_url)

    def test_get_observed_property_ids(self):
        # Create a ThingsSearchModel instance
        search_params = query_analysis.ThingsSearchModel(
                state='CA',
                county='Los Angeles',
                active=True,
                monitoring_location_type='Stream',
                observed_property='Discharge')
            
        # Create a ThingsSearchUrl instance
        search_url = query_analysis.ThingsSearchUrl(search_params)

        # Call the get_observed_property_id method
        result = search_url.get_observed_property_id()
        
        # Check the result
        expected_id_dict = {
            '00060': 'Discharge, cubic feet per second',
            '00061': 'Discharge, instantaneous, cubic feet per second',
            '30208': 'Discharge, cubic meters per second',
            '50042': 'Discharge, gallons per minute',
            '72137': 'Discharge, tidally filtered, cubic feet per second'
            }
        self.assertEqual(result, expected_id_dict)

    def test_get_observed_property_filter_str(self):
        # Create a ThingsSearchModel instance
        search_params = query_analysis.ThingsSearchModel(
                state='CA',
                county='Los Angeles',
                active=True,
                monitoring_location_type='Stream',
                observed_property='Discharge')
            
        # Create a ThingsSearchUrl instance
        search_url = query_analysis.ThingsSearchUrl(search_params)

        # Call the get_observed_property_filter method
        result = search_url.get_observed_property_filter_str()
        
        # Check the result
        expected_filter = []
        for id in ['00060', '00061', '30208', '50042', '72137']:
            expected_filter.append(f"Datastreams/ObservedProperty/@iot.id eq {id}")
        expected_filter = f"({(' or '.join(expected_filter))})"
        self.assertEqual(result, expected_filter)

    def test_construct_url_1(self):
        # Create a ThingsSearchModel instance
        search_params = query_analysis.ThingsSearchModel(
                state='CA',
                county='Los Angeles',
                active=True,
                monitoring_location_type='Stream',
                observed_property=None)
            
        # Create a ThingsSearchUrl instance
        search_url = query_analysis.ThingsSearchUrl(search_params)

        # Call the construct_url method
        search_url.construct_url()

        result = search_url.url
        
        # Check the result
        expected_url = f"https://labs.waterdata.usgs.gov/sta/v1.1/Things?$filter=(properties/state eq 'CA' and properties/county eq 'Los Angeles' and properties/active eq True and properties/monitoringLocationType eq 'Stream')&$count=true"
        self.assertEqual(result, expected_url)

    def test_construct_url_2(self):

        self.maxDiff = None
        # Create a ThingsSearchModel instance
        search_params = query_analysis.ThingsSearchModel(
                state='CA',
                county='Los Angeles',
                active=True,
                monitoring_location_type='Stream',
                observed_property='Discharge')
            
        # Create a ThingsSearchUrl instance
        search_url = query_analysis.ThingsSearchUrl(search_params)

        # Call the construct_url method
        search_url.construct_url()

        result = search_url.url
        
        # Check the result
        expected_url = "https://labs.waterdata.usgs.gov/sta/v1.1/Things" \
            "?$filter=(properties/state eq 'CA' and properties/county eq 'Los Angeles' and properties/active eq True and properties/monitoringLocationType eq 'Stream')"


        observed_property_filter = []
        for id in ['00060', '00061', '30208', '50042', '72137']:
            observed_property_filter.append(f"Datastreams/ObservedProperty/@iot.id eq {id}")
        observed_property_filter = f"({(' or '.join(observed_property_filter))})"

        expected_url += f" and {observed_property_filter}&$count=true"

        self.assertEqual(result, expected_url)

if __name__ == '__main__':
    unittest.main()