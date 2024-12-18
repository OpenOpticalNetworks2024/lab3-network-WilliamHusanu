import json
from core.parameters import c
from core.parameters import c1
import math
import matplotlib.pyplot as plt
from core.math_utils import snr
import pandas as pd


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

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self,value_latency : float):
        self._latency = value_latency

    def update_latency(self,increment_latency : float):
        self._latency += increment_latency

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self,setted_path:list):
        self._path = setted_path

    def update_path(self):
        tmp_list_path = [self._path[0][1:]]
        self._path = tmp_list_path


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


    def propagate(self,signal_info : Signal_information):
        if(len(signal_info._path[0]) != 1):
            id_line = signal_info.path[0][0] + signal_info.path[0][1]
            signal_info.update_path()
            return id_line
        else:
            signal_info.update_path()
            id_line = "XX"
            return id_line

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
        latency_gen = self._len_line / (c1 * 2 / 3)
        return latency_gen

    def noise_generation(self,signal_power:float):
        noise_gen = 1e-9 * signal_power * self._len_line
        return noise_gen
    def propagate(self,sig_info : Signal_information):
        latency = self.latency_generation()
        noise = self.noise_generation(sig_info.signal_power)
        sig_info.update_latency(latency)
        sig_info.update_noise_power(noise)
        id_node = sig_info.path[0][0]
        return id_node







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


        self.connect()

        #creation of dataframe
        path_separ = "->"
        tabel = []
        column_list = ["path", "total latency", "total noise", "SNR [dB]"]

        for id_node1 in self._nodes:
            for id_node2 in self._nodes:
                if(id_node1 != id_node2):
                    for path in self.find_paths(id_node1,id_node2):
                        total_latency = 0
                        total_noise = 0
                        #print(path)
                        #print(len(path))

                        for length in range(len(path)):
                            if(length < len(path) - 1):
                                #adding noise and latency for every path
                                id_line = path[length] + path[length+1]
                                total_latency = self._lines[id_line].latency_generation() + total_latency
                                total_noise = self._lines[id_line].noise_generation(0.001) + total_noise
                                #print(id_line)


                        if(total_noise != 0):
                           snr_evaluated = snr(total_noise)
                           row_list =  [path_separ.join(path), total_latency,total_noise,snr_evaluated]
                           tabel.append(row_list)

        self._dataframe = pd.DataFrame(tabel, columns=column_list)
        print(self._dataframe)


    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def draw(self,file:str):
        pass
        for id_node in self._nodes:
            x0 = self._nodes[id_node].position[0]
            y0 = self._nodes[id_node].position[1]
            plt.plot(x0,y0,'yo',markersize=10)
            plt.text(x0+20,y0+20,id_node)

            for con_node in self._nodes[id_node].connected_nodes:
                x1 = self._nodes[con_node].position[0]
                y1 = self._nodes[con_node].position[1]
                plt.plot([x0,x1],[y0,y1],'r')

        plt.title('Network')
        plt.xlabel('x [m]')
        plt.ylabel('y [m]')
        plt.grid()
        plt.savefig(file,dpi=150)


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
                #if not I have to scan the connected_node of target
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
                #if not I have to scan using the connected node of the connected node of target
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
            tmp_dic = {}
            tmp_dic[id_node] = []
            for id_line in self._lines:
                # Comparison between the Node and the first char of the string Line
                if(id_node == self._lines[id_line].label[0]):
                    #self._nodes[id_node].successive = tmp_dict_id_line_successive
                    tmp_dic[id_node].append(id_line)
            self._nodes[id_node].successive = tmp_dic[id_node]
            #self._nodes[id_node].successive.update({id_node:tmp_dic[id_node]})

        #implementing successive of lines
        for id_line in self._lines:
            for id_node in self._nodes:
                if(id_node == self._lines[id_line].label[1]):
                    self._lines[id_line].successive = id_node

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        #choosing the first and last char of path
        start_node = signal_information._path[0][0]
        final_node = signal_information._path[0][-1]
        #check if the path can exist
        if(signal_information._path[0] in self.find_paths(start_node,final_node)):
            #call the propagate of node
            id_node = start_node
            while(signal_information._path[0][0] != final_node):
                id_line = self._nodes[id_node].propagate(signal_information)
                #call the propagate of line
                id_node = self._lines[id_line].propagate(signal_information)

            #last call of propagate node so the path list is empty
            id_line = self.nodes[id_node].propagate(signal_information)
            #Delete the # for check if the list is empty
            #print(signal_information._path)

        return signal_information
