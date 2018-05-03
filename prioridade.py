#!/usr/bin/env python
# -*- coding: utf-8 -*-
from escalonador import Escalonador
from termcolor import colored


class Prioridade(Escalonador):
    def __init__(self, file):
        super().__init__(file)
        self.cabecalho = 'Tempo\tProcessos (P_# / Prioridade / tempo_total ms / tempo_restante ms)'
        self.cabecalho_efeitos = (colored(self.cabecalho,'cyan', None, ['bold']))
        self.timeline_linhas.append(self.cabecalho_efeitos)

    def escalonar(self):
        if self.quantidade_estado('Pronto') == 0:
            return None

        key = self.maior_prioridade()

        self.processo_executando = key

        return self.processando[self.processo_executando]

    def maior_prioridade(self):
        menor = None
        for i in range(len(self.processando)):
            if self.processando[i].estado == 'Pronto':
                menor = i
                break
        for i in range(len(self.processando)):
            if self.processando[i].estado == 'Pronto':
                if (self.processando[i].prioridade < self.processando[menor].prioridade) and (self.processando[i].estado == 'Pronto'):
                        menor = i
        return menor

    def executar(self, processo):
        if processo.tipo == 'user':
            processo.tempo_de_entrada = self.timeline
        processo.estado = 1
        quant_processos = len(self.processando)
        atualizar_saida = True
        novo_processo = False
        while processo.estado == 'Executando' and not novo_processo:
            if atualizar_saida:
                atualizar_saida = False
                self.mostrar_timeline()
            self.timeline += 1
            self.verificar_entrada_de_processos()
            if (len(self.processando)) > quant_processos:
                quant_processos = len(self.processando)
                atualizar_saida = True
                novo_processo = True
            if processo.tipo == 'user':
                processo.tempo_executado = 1
                if (processo.eventos_I_O > 0 and processo.tempo_restante > 0 and processo.tempo_executado % processo.eventos_I_O == 0):
                    processo.estado = 2
                    self.GER_I_O.estado = 0
                if processo.tempo_restante == 0:
                    processo.estado = 3
                    atualizar_saida = True
                elif novo_processo:
                    processo.estado = 0
            elif processo.tipo == 'system':
                if self.quantidade_estado('Bloqueado para I/O') == 0:
                    processo.estado = 4
                else:
                    self.simular_I_O()
            processo.tempo_de_saida = self.timeline
            self.atraso_ms()

    def montar_linhas(self):
        linha = '{:02d}\t'.format(self.timeline)
        for i in range(len(self.processando)):
            if self.processando[i].estado:
                if self.processando[i].tipo == 'user':
                    aux = 'P_{0.id} / {0.prioridade} / {0.tempo_total:02d}ms / {0.tempo_restante:02d}ms'.format(self.processando[i])
                else:
                    aux = 'P_{0.id} / {0.prioridade} / Tratamento de I/O'.format(self.processando[i])
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
