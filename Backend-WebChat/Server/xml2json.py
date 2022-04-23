
# -*- coding:utf8 -*-
# modify by https://github.com/hay/xml2json/blob/master/xml2json.py
import xml.etree.cElementTree as ET
import json
from ct import *

class Xml2json():

    def __init__(self):
        pass

    def strip_tag(self,tag):
        strip_ns_tag = tag
        split_array = tag.split('}')
        if len(split_array) > 1:
            strip_ns_tag = split_array[1]
            tag = strip_ns_tag
        return tag


    def elem_to_internal(self,elem, strip_ns=1, strip=1):
        """Convert an Element into an internal dictionary (not JSON!)."""

        d = {}
        elem_tag = elem.tag
        if strip_ns:
            elem_tag = self.strip_tag(elem.tag)
        else:
            for key, value in list(elem.attrib.items()):
                d['@' + key] = value

        # loop over subelements to merge them
        for subelem in elem:
            v = self.elem_to_internal(subelem, strip_ns=strip_ns, strip=strip)

            tag = subelem.tag
            if strip_ns:
                tag = self.strip_tag(subelem.tag)

            value = v[tag]

            try:
                # add to existing list for this tag
                d[tag].append(value)
            except AttributeError:
                # turn existing entry into a list
                d[tag] = [d[tag], value]
            except KeyError:
                # add a new non-list entry
                d[tag] = value
        text = elem.text
        tail = elem.tail
        if strip:
            # ignore leading and trailing whitespace
            if text:
                text = text.strip()
            if tail:
                tail = tail.strip()

        if tail:
            d['#tail'] = tail

        if d:
            # use #text element if other attributes exist
            if text:
                d["#text"] = text
        else:
            # text is the value if no attributes
            d = text or None
        return {elem_tag: d}


    def internal_to_elem(self,pfsh, factory=ET.Element):

        """Convert an internal dictionary (not JSON!) into an Element.
        Whatever Element implementation we could import will be
        used by default; if you want to use something else, pass the
        Element class as the factory parameter.
        """

        attribs = {}
        text = None
        tail = None
        sublist = []
        tag = list(pfsh.keys())
        #print pfsh
        #print "-"*100
        if len(tag) != 1:
            raise ValueError("Illegal structure with multiple tags: %s" % tag)
        tag = tag[0]
        value = pfsh[tag]
        if isinstance(value, dict):
            for k, v in list(value.items()):
                if k[:1] == "@":
                    attribs[k[1:]] = v
                elif k == "#text":
                    text = v
                elif k == "#tail":
                    tail = v
                elif k[0] == "$":
                    k = k[1:]
                    v = r'<![CDATA[%s]]>'%v
                    sublist.append(self.internal_to_elem({k: v}, factory=factory))

                elif isinstance(v, list):
                    for v2 in v:
                        sublist.append(self.internal_to_elem({k: v2}, factory=factory))
                else:
                    sublist.append(self.internal_to_elem({k: v}, factory=factory))
        else:
            text = value

        e = factory(tag, attribs)

        for sub in sublist:
            e.append(sub)

        e.text = text
        e.tail = tail
        return e


    def elem2json(self,elem, strip_ns=1, strip=1):

        """Convert an ElementTree or Element into a JSON string."""

        if hasattr(elem, 'getroot'):
            elem = elem.getroot()

        #if options.pretty:
        return json.dumps(self.elem_to_internal(elem, strip_ns=strip_ns, strip=strip), sort_keys=True, indent=4, separators=(',', ': '))
        #else:
        #return json.dumps(self.elem_to_internal(elem, strip_ns=strip_ns, strip=strip))


    def json2elem(self,json_data, factory=ET.Element):

        """Convert a JSON string into an Element.
        Whatever Element implementation we could import will be used by
        default; if you want to use something else, pass the Element class
        as the factory parameter.
        """

        return self.internal_to_elem(json.loads(json_data), factory)


    def xml2json(self,xmlstring,strip_ns=1, strip=1):

        """Convert an XML string into a JSON string."""

        elem = ET.fromstring(xmlstring)
        return self.elem2json(elem, strip_ns=strip_ns, strip=strip)


    def json2xml(self,json_data, factory=ET.Element):

        """Convert a JSON string into an XML string.
        Whatever Element implementation we could import will be used by
        default; if you want to use something else, pass the Element class
        as the factory parameter.
        """
        if not isinstance(json_data, dict):
            json_data = json.loads(json_data)

        elem = self.internal_to_elem(json_data, factory)
        return ET.tostring(elem)

class recv_reply_action():
    def __init__(self):

        pass

    def getRec(self,data):
        self.xml_recv = ET.fromstring(data)
        return self.xml_recv.find(name).text

    def doAction(self):

        pass

    def getRes(self,type,dic):
        if type == MT_T:

            pass
        elif type == MT_I:

            pass
        else:
            pass


