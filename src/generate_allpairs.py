#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartDrive Motors - Generador y Verificador de Suites All-Pairs (Pairwise Testing)
Módulo para el Taller Autónomo de Modelado Combinatorio y All-Pairs (Clase 09 - Bloque 2)
Integrantes: Daniel Cadena, Gonzalo Cárdenas, Gabriel Vasquez
"""

import sys
from itertools import combinations
from allpairspy import AllPairs

# Definición formal de Parámetros y Valores (P&V)
PARAMETERS = {
    "Motor": ["Gasolina", "Híbrido", "Eléctrico"],
    "Transmisión": ["Manual", "Automática", "Monomarcha"],
    "Frenos": ["Estándar", "ABS", "Regenerativo"],
    "Mercado": ["América", "Europa", "Asia"],
    "Modo": ["Eco", "Sport", "Autónomo"]
}

PARAM_KEYS = list(PARAMETERS.keys())
PARAM_VALUES = [PARAMETERS[k] for k in PARAM_KEYS]

def calculate_exhaustive_combinations():
    total = 1
    for k, v in PARAMETERS.items():
        total *= len(v)
    return total

def get_all_target_pairs():
    target_pairs = set()
    for p1, p2 in combinations(PARAM_KEYS, 2):
        for v1 in PARAMETERS[p1]:
            for v2 in PARAMETERS[p2]:
                target_pairs.add(((p1, v1), (p2, v2)))
    return target_pairs

def evaluate_coverage(test_suite, all_target_pairs):
    covered_pairs = set()
    for test in test_suite:
        row_dict = dict(zip(PARAM_KEYS, test))
        for p1, p2 in combinations(PARAM_KEYS, 2):
            pair = ((p1, row_dict[p1]), (p2, row_dict[p2]))
            covered_pairs.add(pair)
    coverage_pct = (len(covered_pairs) / len(all_target_pairs)) * 100.0
    return covered_pairs, coverage_pct

def constraint_filter(row):
    """
    Evalúa si una combinación parcial o completa cumple las restricciones lógicas.
    """
    n = len(row)
    motor = row[0] if n > 0 else None
    trans = row[1] if n > 1 else None
    frenos = row[2] if n > 2 else None
    mercado = row[3] if n > 3 else None
    modo = row[4] if n > 4 else None

    # Regla 1: Motor Eléctrico implica Transmisión Monomarcha y Frenos Regenerativos
    if motor == "Eléctrico":
        if trans is not None and trans != "Monomarcha":
            return False
        if frenos is not None and frenos != "Regenerativo":
            return False

    # Regla 2: Motor Gasolina no permite Frenos Regenerativos
    if motor == "Gasolina":
        if frenos is not None and frenos == "Regenerativo":
            return False
        # Regla 3: Motor Gasolina requiere caja multivelocidad (no monomarcha)
        if trans is not None and trans == "Monomarcha":
            return False

    # Regla 4: Conducción Autónoma requiere actuadores compatibles (no caja manual, no freno mecánico estándar)
    if modo == "Autónomo":
        if trans is not None and trans == "Manual":
            return False
        if frenos is not None and frenos == "Estándar":
            return False

    return True

def generate_suites():
    # 1. Generación Pura All-Pairs
    pure_suite = list(AllPairs(PARAM_VALUES))
    
    # 2. Generación con Constraints All-Pairs
    constrained_suite = list(AllPairs(PARAM_VALUES, filter_func=constraint_filter))
    
    return pure_suite, constrained_suite

if __name__ == "__main__":
    exhaustive_count = calculate_exhaustive_combinations()
    target_pairs = get_all_target_pairs()
    pure_suite, constrained_suite = generate_suites()
    covered, coverage_pct = evaluate_coverage(pure_suite, target_pairs)

    print("==================================================")
    print("CONFIGURADOR SMARTDRIVE MOTORS - ANÁLISIS COMBINATORIO")
    print("==================================================")
    print(f"Combinaciones exhaustivas puras (3^5): {exhaustive_count}")
    print(f"Total de pares únicos teóricos a cubrir: {len(target_pairs)}")
    print(f"Casos generados en Suite Pura All-Pairs: {len(pure_suite)}")
    print(f"Pares cubiertos en Suite Pura: {len(covered)} / {len(target_pairs)} ({coverage_pct:.2f}%)")
    print(f"Casos generados con Restricciones de Negocio: {len(constrained_suite)}")
    print("\n--- SUITE PURA ALL-PAIRS ---")
    print("| Test Case | Motor | Transmisión | Frenos | Mercado | Modo |")
    print("|-----------|-------|-------------|--------|---------|------|")
    for i, row in enumerate(pure_suite, 1):
        print(f"| TC-{i:02d} | {' | '.join(row)} |")

    print("\n--- SUITE CON RESTRICCIONES (CONSTRAINTS) ---")
    print("| Test Case | Motor | Transmisión | Frenos | Mercado | Modo |")
    print("|-----------|-------|-------------|--------|---------|------|")
    for i, row in enumerate(constrained_suite, 1):
        print(f"| TC-C{i:02d} | {' | '.join(row)} |")
