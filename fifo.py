#!/usr/bin/env python
# -*- coding: utf-8 -*-
from escalonador import Escalonador
from termcolor import colored


class FIFO(Escalonador):
    def __init__(self, file):
        super().__init__(file)
        self.cabecalho = 'Tempo\tProcessos (P_# / tempo_total ms / tempo_restante ms)'
        self.cabecalho_efeitos = (colored(self.cabecalho,'cyan', None, ['bold']))
        self.timeline_linhas.append(self.cabecalho_efeitos)

    def escalonar(self):
        if self.processo_executando == 0:
            self.processo_executando = 1
            self.processando[self.processo_executando].estado = 1
            return self.processando[self.processo_executando]

        if self.quantidade_estado('Pronto') == 0:
            return None

        key = (self.processo_executando+1)

        while self.processando[key].estado != 'Pronto':
            key += 1

        if ((key) == (len(self.processando))):
            return None

        if key != self.processo_executando:
            self.processo_executando = key

        return self.processando[key]

    def executar(self, processo):
        if processo.tipo == 'user':
            processo.tempo_de_entrada = self.timeline
        processo.estado = 1
        quant_processos = len(self.processando)
        atualizar_saida = True
        while processo.tempo_restante > 0:
            if atualizar_saida:
                atualizar_saida = False
                self.mostrar_timeline()
            self.timeline += 1
            self.verificar_entrada_de_processos()
            if (len(self.processando)) > quant_processos:
                quant_processos = len(self.processando)
                atualizar_saida = True
            processo.tempo_executado = 1
            if (processo.eventos_I_O > 0 and processo.tempo_restante > 0):
                processo.estado = 2
                processo.tempo_de_saida = self.timeline
                self.GER_I_O.estado = 1
                self.mostrar_timeline()
                atualizar_saida = False
                while processo.eventos_I_O > 0:
                    processo._Processo__eventos_I_O -= 1
                    # processo._Processo__tempo_de_espera += 1
                    self.timeline += 1
                    self.atraso_ms()
                processo.estado = 1
                self.GER_I_O.estado = 4
                processo.tempo_de_entrada = self.timeline
                self.mostrar_timeline()
            if processo.tempo_restante == 0:
                processo.estado = 3
                atualizar_saida = True
            self.atraso_ms()

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
