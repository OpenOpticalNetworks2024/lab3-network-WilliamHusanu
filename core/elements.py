import json

from core.parameters import c
import math


class Signal_information(object):
    def __init__(self,sp:float,pth:list):
        self._signal_power = sp
        self._noise_power = 0.0
        self._latency = 0.0
        self._path = pth

    @property
    def signal_power(self):
        return self._signal_power

    def update_signal_power(self,increment_sp:float):
        self._signal_power += increment_sp
        print("Signal_power :", self._signal_power)

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self,value_np:float):
        self._noise_power = value_np

    def update_noise_power(self,increment_np:float):
        self._noise_power += increment_np
        print("Noise_power :", self._noise_power)

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self,value_latency : float):
        self._latency = value_latency

    def update_latency(self,increment_latency : float):
        self._latency += increment_latency
        print("Latency :", self._latency)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self,setted_path:list):
        self._path = setted_path

    def update_path(self):
        pass


class Node(object):
    def __init__(self,id_node:str,pos_nod:tuple[float,float],con_nod:list):
        self._id_node = id_node
        self._pos_nod = pos_nod
        self._con_nod = con_nod
        self._successive_node = {}

    @property
    def label(self):
        return self._id_node

    @property
    def position(self):
        return self._pos_nod

    @property
    def connected_nodes(self):
        return self._con_nod

    @property
    def successive(self):
        return self._successive_node

    @successive.setter
    def successive(self,successive_line):
        self._successive_node = successive_line


    def propagate(self):
        pass


class Line(object):
    def __init__(self,id_line:str,len_line:float):
        self._id_line = id_line
        self._len_line = len_line
        self._successive_line = {}

    @property
    def label(self):
        return self._id_line

    @property
    def length(self):
        return self._len_line

    @property
    def successive(self):
        return self._successive_line

    @successive.setter
    def successive(self,successive_node):
        self._successive_line = successive_node

    def latency_generation(self):
        latency_gen = self._len_line / (c * 2 / 3)
        return latency_gen
        #print(latency_gen)

    def noise_generation(self,signal_power:float):
        noise_gen = 1e-9 * signal_power * self._len_line
        return noise_gen
    def propagate(self,sig_info : Signal_information):
        laty = self.latency_generation()
        noisy = self.noise_generation(sig_info.signal_power)

        sig_info.update_noise_power(noisy)
        sig_info.update_latency(laty)







class Network(object):
    def __init__(self,file : str):
        self._nodes = {}
        self._lines = {}
        file_json = json.load(open(file,'r'))
        #saving nodes
        for id_node in file_json:
            #Inside self._nodes[id_node],saving the information about label,position and connected_nodes
            self._nodes[id_node] = Node(id_node,file_json[id_node]['position'],file_json[id_node]['connected_nodes'])

        for id_node in self._nodes:
            #set the position of the First node ( First iterate : A )
            position_1 = self._nodes[id_node].position
            for con_node in self._nodes[id_node].connected_nodes:
                #set the position of the Second node ( First iterate : B )
                position_2 = self._nodes[con_node].position
                #check the two lengths and verify which is the min
                leng_1 = math.sqrt((position_2[0]-position_1[0])**2 + (position_2[1]-position_1[1])**2)
                leng_2 = math.sqrt((position_1[0]-position_2[0])**2 + (position_1[1]-position_2[1])**2)
                leng = min(leng_1,leng_2)
                #creating the label for Line
                id_line = id_node + con_node
                #creating the Line
                self._lines[id_line] = Line(id_line,leng)



    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def draw(self):
        pass

    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, label1, label2):
        found_paths = []
        found_paths_final = []

        for id_line in self._lines:
            if(self._lines[id_line].label[0] == label1):
                #selecting the end of my starting line
                target = self._lines[id_line].label[1]
                #if my target is label2
                if(target == label2):
                    found_paths.append(id_line)
                #if not i have to scan the connected_node of target
                else:
                    for con_node in self._nodes[target].connected_nodes:
                        if(label1 != con_node):
                            found_paths.append(label1+target+con_node)

        #created here a list just to help me in the scanning
        for id_list in found_paths:
            len_tmp_list = len(id_list)
            if(id_list[0] == label1)and(id_list[len_tmp_list-1] == label2):
                #if label2 is already in the string inside the list
                found_paths_final.append(id_list)
            else:
                #if not i have to scan using the connected node of the connected node of target
                for con_node in self._nodes[id_list[len_tmp_list-1]].connected_nodes:
                    if(not(con_node in id_list)):
                        if(con_node == label2):
                            found_paths_final.append(id_list+label2)
                        else:
                            for con_con_node in self._nodes[con_node].connected_nodes:
                                if(not(con_node in id_list)):
                                    if(not(con_con_node in id_list)):
                                        if(con_con_node == label2):
                                            found_paths_final.append(id_list+con_node+con_con_node)
                                        else:
                                            for con_con_con_node in self._nodes[con_con_node].connected_nodes:
                                                list_tmp = id_list+con_node+con_con_node
                                                if(not(con_con_con_node in list_tmp)):
                                                    if (con_con_con_node == label2):
                                                        found_paths_final.append(list_tmp+con_con_con_node)
        return found_paths_final



















    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):

        #implementing successive of node
        for id_node in self._nodes:
            for id_line in self._lines:
                # Comparison between the Node and the first char of the string Line
                if(id_node == self._lines[id_line].label[0]):
                    self._nodes[id_node].successive = id_line


        #implementing successive of lines
        for id_line in self._lines:
            for id_node in self._nodes:
                if(id_node == self._lines[id_line].label[1]):
                    self._lines[id_line].successive = id_node

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        pass