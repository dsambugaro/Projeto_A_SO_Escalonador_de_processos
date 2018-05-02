#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sys import argv, exit
from termcolor import colored

from round_robin import Round_Robin
from fifo import FIFO
from shortest_job_first import SJF
from prioridade import Prioridade
from shortest_remaining_time import SRT

def help():
    print('\n\n')
    print('Uso:\t{} [{}] [{}] [{}] \n\n'.format(argv[0], colored('ARQUIVO_COM_PROCESSOS', 'white', None, ['bold']), colored('ALGORITMO', 'white', None, ['bold']), colored('QUANTUM', 'white', None, ['bold'])))
    print('Descrição:\tSimula um escalonador de processos com o algoritmo definido.\n\t\tPara propósitos didáticos cada ms dos processos dura cerca de 200ms\n\n')
    print('OPÇÕES:\n')
    print('\t{} - Um arquivo .txt contendo os processos a serem carregados no simulador. Cada linha representa um processo que deve seguir o seguinte formato: \n\t\t\"id tempo_de_execucao prioridade tempo_de_chegada eventos_I_O_1 eventos_I_O_2 ... eventos_I_O_N\"\n\n'.format(format(colored('ARQUIVO_COM_PROCESSOS', 'white', None, ['bold']))))
    print('\t{} - algoritmo de escalonamento a ser simulado, asopções disponiveis são:\n\t\tRR (Round-Robin)\n\t\tFIFO (First In First Out)\n\t\tSJF (Shortest Job First)\n\t\tSRT (Shortest Remaining Time)\n\t\tPrioridade\n\n'.format(format(colored('ALGORITMO', 'white', None, ['bold']))))
    print('\t{} - Apenas é exigido para execução do algoritmo RR (Round-Robin)\n\n'.format(format(colored('QUANTUM', 'white', None, ['bold']))))
    print('\t{} - Exibe essa ajuda e sai'.format(format(colored('help', 'white', None, ['bold']))))
    print('\n\n')

if __name__ == '__main__':
    try:
        algoritmos = ['RR', 'FIFO', 'SJF', 'SRT', 'Prioridade']
        if argv[1] == 'help':
            help()
            exit(0)
        elif argv[2] in algoritmos:

            algoritmo = argv[2]
            processos = argv[1]
            if algoritmo == 'RR':
                quantum = argv[3]

            if algoritmo == 'RR':
                os.system('clear')
                RR = Round_Robin(processos, quantum)
                RR.simular_escalonamento()
            elif algoritmo == 'FIFO':
                FIFO = FIFO(processos)
                os.system('clear')
                FIFO.simular_escalonamento()
            elif algoritmo == 'SJF':
                SJF = SJF(processos)
                os.system('clear')
                SJF.simular_escalonamento()
            elif algoritmo == 'SRT':
                SRT = SRT(processos)
                os.system('clear')
                SRT.simular_escalonamento()
            elif algoritmo == 'Prioridade':
                os.system('clear')
                Prioridade = Prioridade(processos)
                Prioridade.simular_escalonamento()
            else:
                help()
                exit(1)
        else:
            print('\n{}'.format(colored('Opções inválidas', 'red', None, ['bold'])))
            help()
            exit(1)
    except IndexError:
        print('\n{}\n'.format(colored('Opções inválidas', 'red', None, ['bold'])))
        help()
        exit(1)
