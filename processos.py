#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep

class Processo(object):
    __estados = {0: 'Pronto',
                 1: 'Executando',
                 2: 'Bloqueado para I/O',
                 3: 'Concluído',
                 4: 'Suspenso'}

    __estado = None

    __tipos = {0: 'user',
               1: 'system'}

    __tempo_de_saida = None

    __tempo_executado = 0

    __tempo_de_entrada = []

    __tempo_de_espera = 0

    def __init__(self, tipo, id, tempo_total, prioridade, tempo_chegada,
                 eventos_I_O):
        self.tipo = tipo
        self.id = id
        self.tempo_total = tempo_total
        self.__tempo_restante = tempo_total
        self.prioridade = prioridade
        self.tempo_chegada = tempo_chegada
        self.eventos_I_O = eventos_I_O

    @property
    def estado(self):
        return self.__estado

    @property
    def tempo_de_espera(self):
        return self.__tempo_de_espera

    @tempo_de_espera.setter
    def tempo_de_espera(self, tempo_de_espera):
        self.__tempo_de_espera = tempo_de_espera

    @estado.setter
    def estado(self, estado):
        if estado in self.__estados:
            self.__estado = self.__estados[estado]

    @property
    def eventos_I_O(self):
        return self.__eventos_I_O

    @eventos_I_O.setter
    def eventos_I_O(self, eventos_I_O):
        if len(eventos_I_O) != 0:
            taxa_I_O = round(self.tempo_total / len(eventos_I_O))
        else:
            taxa_I_O = 0
        self.__eventos_I_O = taxa_I_O

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo):
        if tipo in self.__tipos:
            self.__tipo = self.__tipos[tipo]

    @property
    def tempo_restante(self):
        return self.__tempo_restante

    @property
    def tempo_executado(self):
        return self.__tempo_executado

    @tempo_executado.setter
    def tempo_executado(self, tempo_executado):
        if ((self.__tempo_restante - tempo_executado) < 0):
            self.__tempo_restante = 0
        else:
            self.__tempo_restante -= tempo_executado
        self.__tempo_executado += tempo_executado

    @property
    def tempo_de_saida(self):
        return self.__tempo_de_saida

    @tempo_de_saida.setter
    def tempo_de_saida(self, tempo_de_saida):
        if tempo_de_saida <= 0:
            self.__tempo_de_saida = 0
        else:
            self.__tempo_de_saida = tempo_de_saida

    @property
    def tempo_de_entrada(self):
        return self.__tempo_de_entrada

    @tempo_de_entrada.setter
    def tempo_de_entrada(self, tempo_de_entrada):
        if tempo_de_entrada == self.tempo_chegada:
            self.__tempo_de_espera += 0
        elif self.tempo_executado == 0:
            self.__tempo_de_espera += (tempo_de_entrada - self.tempo_chegada)
        elif self.tempo_de_saida:
            self.__tempo_de_espera += (tempo_de_entrada - self.tempo_de_saida)
        self.__tempo_de_entrada.append(tempo_de_entrada)

        # print('self.tempo_de_saida: {}'.format(self.tempo_de_saida))
        # print('self.__tempo_de_espera: {}'.format(self.__tempo_de_espera))
        # print('tempo_de_entrada: {}'.format(tempo_de_entrada))
        # sleep(5)
