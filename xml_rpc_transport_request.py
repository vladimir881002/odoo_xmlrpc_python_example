# -*- coding: UTF-8 -*-

import requests
import xmlrpc.client
from time import sleep


class RequestsTransport(xmlrpc.client.Transport):

    def request(self, host, handler, data, verbose=False):
        # set the headers, including the user-agent
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
                   "Content-Type": "text/xml",
                   "Accept-Encoding": "gzip"}
        # url = "https://%s%s" % (host, handler)
        url = "http://%s%s" % (host, handler)
        return self.do_request(url=url, data=data, headers=headers)

    def do_request(self, url, data, headers):
        try:
            response = None
            response = requests.post(url, data=data, headers=headers)
            response.raise_for_status()
            return self.parse_response(response)
        except requests.RequestException as e:
            if response is None:
                print("500--%s" % str(e))
                # raise xmlrpc.client.ProtocolError(url, 500, str(e), "")
            else:
                print("%s--%s" % (response.status_code, str(e)))
                # raise xmlrpc.client.ProtocolError(url, response.status_code,
                #                                   str(e), response.headers)
            print('Sleeping  for to second a resend de request')
            sleep(2.0)
            return self.do_request(url=url, data=data, headers=headers)

    def parse_response(self, resp):
        """
        Parse the xmlrpc response.
        """
        p, u = self.getparser()
        p.feed(resp.text)
        p.close()
        return u.close()