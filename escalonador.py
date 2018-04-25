#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from time import sleep
from processos import Processo
from termcolor import colored


class Escalonador(ABC):
    """
    Classe abstrata para criar simulações de algoritmos de escalonamento.
    Instancia uma lista de processos baseado no arquivo ``file`` que deve ser
    passado
    Necessário implementar
    """
    # Por propositos didáticos, para poder obervar o que está ocorrendo no
    # simulador cada 1ms do tempo de execução do processo durará 500ms
    __delay = 0.5
    __timeline = 0
    processo_executando = 0
    timeline_linhas = []
    descricao = ''

    def __init__(self, file):
        self.processar = self.__parse_file(file)
        self.processando = [Processo(1, 'GER_I_O', 10, 5, None, [])]
        self.processando[0].estado = 4
        self.GER_I_O = self.processando[0]

    def __parse_file(self, file):
        """
        Cria lista de processos com base no arquivo de entrada ``file``
        Formato dos processos no arquivo:
        ``id tempo_de_execucao prioridade tempo_de_chegada eventos_I_O``
        """
        aux = []
        with open(file, "r") as processos:
            for line in processos:
                atributos = line.split()
                aux.append(Processo(0, int(atributos[0]), int(atributos[1]),
                                    int(atributos[2]), int(atributos[3]),
                                    list(map(int, atributos[4:]))))
        return aux

    def atraso_ms(self):
        sleep(self.__delay)

    @property
    def timeline(self):
        """Tempo atual da timeline do escalonador."""
        return self.__timeline

    @timeline.setter
    def timeline(self, timeline):
        self.__timeline = timeline

    @abstractmethod
    def montar_linhas(self):
        raise NotImplementedError("Você não pode instanciar essa classe "
                                  "abstrata. Implemente-a, por favor")

    @abstractmethod
    def escalonar(self):
        raise NotImplementedError("Você não pode instanciar essa classe " +
                                  "abstrata. Implemente-a, por favor")

    @abstractmethod
    def executar(self, processo):
        raise NotImplementedError("Você não pode instanciar essa classe " +
                                  "abstrata. Implemente-a, por favor")

    @abstractmethod
    def simular_I_O(self):
        raise NotImplementedError("Você não pode instanciar essa classe " +
                                  "abstrata. Implemente-a, por favor")

    @abstractmethod
    def simular_escalonamento(self):
        raise NotImplementedError("Você não pode instanciar essa classe " +
                                  "abstrata. Implemente-a, por favor")

    def mostrar_timeline(self):
        self.montar_linhas()
        executando = colored('Executando:', 'yellow', None, ['underline', 'bold'])
        pronto = colored('\tProntos:', 'cyan', None, ['bold'])
        bloqueados = colored('\tBloqueados para I/O:', 'red', None, ['bold'])
        concluidos = colored('\t\tConcluídos:', 'green', None, ['bold'])
        dados = ('{} {:7}{} {:2d} {}{:2d}{} {}\n'.format(executando, self.processando[self.processo_executando].id, pronto, self.quantidade_estado('Pronto'), bloqueados, self.quantidade_estado('Bloqueado para I/O'), concluidos, self.quantidade_estado('Concluído')))
        print('\n\n\n')
        print('Simulação de escalonamento de processos com algoritmo {}'.format(self.__class__.__name__))
        print('{}'.format(self.descricao))
        print('Processos carregados no simulador: {}'.format(len(self.processar)))
        print('\n\n\n')
        print(dados)
        print(''.center(191, '_'))
        print(*self.timeline_linhas, sep='\n')
        if self.quantidade_estado('Concluído')+1 == len(self.processar)+1:
            print('\n\n\n')
            tempo_total = self.tempo_de_espera_total()
            tempo_medio = self.tempo_de_espera_medio()
            print('Tempo total de espera (TTE) = {}'.format(tempo_total))
            print('Tempo médio de espera (TME) = {}'.format(tempo_medio))
            print('\n\n\n')
        else:
            print('', end='\x1b[r', flush = True)

    def verificar_entrada_de_processos(self):
        for i in range((len(self.processando)-1), len(self.processar)):
            if not self.processar[i].estado:
                if self.processar[i].tempo_chegada == self.timeline:
                    self.processar[i].estado = 0
                    self.processando.append(self.processar[i])

    def tempo_de_espera_total(self):
        tempo_de_espera_total = 0
        for i in range(len(self.processando)):
            if self.processando[i].estado == 'Concluído':
                tempo_de_espera_total += (self.processando[i].tempo_de_espera)
        return tempo_de_espera_total

    def tempo_de_espera_medio(self):
        tempo_de_espera_total = self.tempo_de_espera_total()
        tempo_de_espera_medio = (tempo_de_espera_total /
                                 (self.quantidade_estado('Concluído')))
        return tempo_de_espera_medio

    def quantidade_estado(self, estado):
        quantidade = 0
        for i in range(len(self.processando)):
            if self.processando[i].estado == estado:
                quantidade += 1
        return quantidade
