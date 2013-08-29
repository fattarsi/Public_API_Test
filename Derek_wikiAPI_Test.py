
from nose.tools import assert_equal, assert_not_equal
from testconfig import config

from xml.dom.minidom import parse, parseString

import logging

import requests
# We will use the reauests library to simplify invoking the REST API (Requests is HTTP for Humans)


#
# Test automation for WikipediA API : Version of nosetest 1.3.0
#


class wikiAPI_Test:

    logger = logging.getLogger(__name__)


    def __init__(self):
        self.tc_name = self.__class__.__name__
        self.tc_id = self.tc_name[:self.tc_name.index("_")]
        self.logger.info('INIT of test case run for file {0}'.format(self.tc_id))

    @classmethod
    def setup_class(cls):
        '''Class level setup, will run before test case(s), only runs once'''
		# Future use
        cls.logger.info('Setup: Class level: completed.')

    @classmethod
    def teardown_class(cls):
        '''Class level teardown, will run after all the test cases in the test class, only runs once'''
		# Future use
        cls.logger.info('Teardown - class level: completed')


    def setup(self):
        '''Function level setup, will run for each test case in the test class '''
		# Future use
        self.logger.info('Setup - function level: completed')

    def teardown(self):
        '''Function level teardown, will run for each test case in the test class '''
		# Future use
        self.logger.info('Teardown - function level: completed')

    #If we had a nuber of helper functions they could be moved to a util directory (along with the API invokation)

    def get_pageId_fromXML(self, xml_data):
        doc  = parseString(xml_data);
        pages = doc.getElementsByTagName("page")
        return pages[0].getAttribute("pageid")
		

    # # Start of test case TC0001 - verify content header and returned http status code for Piston Cloud Wiki Page

    def TC0001_check_status_and_content_header_test(self):
        self.logger.info('Starting TC0001_check_status_and_content_header_test ......')
		
        # The following test data could be stored in test data directory, config file or feed into a driver routine.  It is placed here for clarity.

        # Test Data for Request :Positive test case
        test_base_url = "http://en.wikipedia.org/w/api.php"  # Wikipedia api endpoint
        payload_data = {'title': 'Piston_Cloud_Computing', 'printable':'yes'}  
        test_header = {'User-agent': 'Mozilla/5.0'}

        # Expected Response data 
        exp_response_content_header = 'text/html; charset=utf-8'
        exp_http_status_code = 200

        # Make request to WikipediA API
        try:
            r = requests.get(test_base_url, params=payload_data, headers=test_header)
            self.logger.info("The REST API returned the follow http status code : {0}".format(r.status_code))
            r.raise_for_status()
        except requests.HTTPError, e:
            self.logger.info("HTTP Error occured : {0}".format(e.message))

        # Verify the returned status code and header content       
        assert_equal(exp_http_status_code, r.status_code, 'ERROR: An unexpected HTTP Status {0} code was returned'.format(r.status_code))  
        assert_equal(exp_response_content_header, r.headers['Content-Type'], 'ERROR: The API returned an unexpected content type {0}'.format(r.headers['Content-Type'])) 


        self.logger.info('End of TC0001_check_status_and_content_header_test ..........')

  
    def TC0002_check_content_header_and_pageid_XMLformat_test(self):
        self.logger.info('Starting  TC0002_check_content_header_and_pageid_XMLformat_test..........')
        
        #The following test data could be stored in test data directory, config file or feed into a driver routine.  It is placed here for clarity.

        #Test Data for Request : Positive test case
        test_base_url = "http://en.wikipedia.org/w/api.php" # WikipediA endpoint
        payload_data =  {'action': 'query', 'prop':'revisions', 'rvprop': 'content','format': 'xml','titles':'Piston_Cloud_Computing'}
        test_header =   {'User-agent': 'Mozilla/5.0'}
    

        #Expected Response data 
        exp_response_content_header = 'text/xml; charset=utf-8'
        exp_http_status_code =  200
        exp_pageid = "38229751"

        # Make request to WikipediA API
        try:
            r = requests.get(test_base_url,params = payload_data, headers=test_header)
            self.logger.info("The REST API returned the follow http status code : {0}".format(r.status_code))
            r.raise_for_status()
        except requests.HTTPError, e:
            self.logger.info("HTTP Error occured : {0}".format(e.message))

        #Verify status code, pageid and pageid results      
        assert_equal(exp_http_status_code, r.status_code, 'ERROR: An unexpected HTTP Status {0} code was returned'.format(r.status_code))  
        assert_equal(exp_response_content_header, r.headers['Content-Type'],  'ERROR: The API returned an unexpected content type {0}'.format(r.headers['Content-Type'])) 
        assert_equal(exp_pageid,self.get_pageId_fromXML(r.content), 'ERROR: Bad pageid was returned' )

        self.logger.info('End of TC0002_check_content_header_and_pageid_XMLformat_test ..........')
        
    def TC0003_check_invalid_titles_XMLformat_test(self):
        self.logger.info('TC0003_check_invalid_titles_XMLformat_test ..........')
        
        #The following test data could be stored in test data directory, config file or feed into a driver routine.  It is placed here for clarity.

        #Test Data for Request : Negative test case
        test_base_url = "http://en.wikipedia.org/w/api.php" # WikipediA endpoint
        payload_data =  {'action': 'query', 'prop':'revisions', 'rvprop': 'content','format': 'xml','titles':'Piston_Cloud_Cookies'}
        test_header =   {'User-agent': 'Mozilla/5.0'}
    

        #Expected Response data 
        exp_response_content_header = 'text/xml; charset=utf-8'
        exp_http_status_code =  200
        exp_pageid = "38229751"

        # Make request to WikipediA API
        try:
            r = requests.get(test_base_url,params = payload_data, headers=test_header)
            self.logger.info("The REST API returned the follow http status code : {0}".format(r.status_code))
            r.raise_for_status()
        except requests.HTTPError, e:
            self.logger.info("HTTP Error occured : {0}".format(e.message))

        #Check status code, pageid and pageid results      
        assert_equal(exp_http_status_code, r.status_code, 'ERROR: An unexpected HTTP Status {0} code was returned'.format(r.status_code))  
        assert_equal(exp_response_content_header, r.headers['Content-Type'],  'ERROR: The API returned an unexpected content type {0}'.format(r.headers['Content-Type'])) 
        assert_not_equal(exp_pageid,self.get_pageId_fromXML(r.content), 'ERROR: Wrong pageid was returned' )

        self.logger.info('End of TC0003_check_invalid_titles_XMLformat_test ..........')



        
        


