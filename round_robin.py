#!/usr/bin/env python
# -*- coding: utf-8 -*-
from escalonador import Escalonador
from termcolor import colored


class Round_Robin(Escalonador):
    __tempo_executando = 0

    def __init__(self, file, quantum):
        self.quantum = quantum
        self.descricao = 'Quantum: {}'.format(self.quantum)
        super().__init__(file)
        self.cabecalho = 'Tempo\tProcessos (P_# / tempo_total ms / tempo_restante ms)'
        self.cabecalho_efeitos = (colored(self.cabecalho,'cyan', None, ['bold']))
        self.timeline_linhas.append(self.cabecalho_efeitos)

    def escalonar(self):

        if self.quantidade_estado('Pronto') == 0:
            return None

        key = ((self.processo_executando+1) % len(self.processando))
        while self.processando[key].estado != 'Pronto':
            key = ((key+1) % len(self.processando))

        if key != self.processo_executando:
            self.processo_executando = key

        return self.processando[key]

    def executar(self, processo):
        self.__tempo_executando = 0
        if processo.tipo == 'user':
            processo.tempo_de_entrada = self.timeline
        processo.estado = 1
        quant_processos = len(self.processando)
        atualizar_saida = True
        while self.__tempo_executando != self.quantum and processo.estado == 'Executando':
            if atualizar_saida:
                atualizar_saida = False
                self.mostrar_timeline()
            self.__tempo_executando += 1
            self.timeline += 1
            self.verificar_entrada_de_processos()
            if (len(self.processando)) > quant_processos:
                quant_processos = len(self.processando)
                atualizar_saida = True
            if processo.tipo == 'user':
                processo.tempo_executado = 1
                if ((processo.eventos_I_O > 0) and (processo.tempo_executado % processo.eventos_I_O) == 0) and (processo.tempo_restante > 0):
                    processo.estado = 2
                    self.GER_I_O.estado = 0
                if processo.tempo_restante == 0:
                    processo.estado = 3
            elif processo.tipo == 'system':
                if self.quantidade_estado('Bloqueado para I/O') == 0:
                    processo.estado = 4
                else:
                    self.simular_I_O()
            self.atraso_ms()
        processo.tempo_de_saida = (self.timeline+1)
        if processo.estado == 'Executando':
            processo.estado = 0

    def simular_I_O(self):
        for i in range(len(self.processando)):
            if self.processando[i].estado == 'Bloqueado para I/O':
                self.processando[i].estado = 0
                break

    def simular_escalonamento(self):
        self.verificar_entrada_de_processos()
        while self.quantidade_estado('Concluído') < len(self.processar):
            processo = self.escalonar()
            if processo != None:
                self.executar(processo)
            else:
                self.timeline += 1
                self.verificar_entrada_de_processos()
                self.mostrar_timeline()
        self.mostrar_timeline()

    def montar_linhas(self):
        linha = '{:02d}\t'.format(self.timeline)
        for i in range(len(self.processando)):
            if self.processando[i].estado:
                if self.processando[i].tipo == 'user':
                    aux = 'P_{0.id} / {0.tempo_total:02d}ms / {0.tempo_restante:02d}ms'.format(self.processando[i])
                else:
                    aux = 'P_{0.id} / Tratamento de I/O'.format(self.processando[i])
                if self.processando[i].estado == 'Pronto':
                    aux = colored(aux, 'cyan', None, ['bold'])
                elif self.processando[i].estado == 'Executando':
                    aux = colored(aux, 'yellow', None, ['underline', 'bold'])
                elif self.processando[i].estado == 'Bloqueado para I/O':
                    aux = colored(aux, 'red', None, ['bold'])
                elif self.processando[i].estado == 'Concluído':
                    aux = colored(aux, 'green', None, ['bold'])
                elif self.processando[i].estado == 'Suspenso':
                    aux = colored(aux, 'cyan', None, ['dark'])
                linha += aux
                linha += ' | '
        self.timeline_linhas.append(linha)
