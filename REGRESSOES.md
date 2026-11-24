# Verificação dos testes de regressão

| Marco / issue | Teste executado contra o comportamento original | Resultado original | Resultado corrigido |
|---|---|---|---|
| 1 / #4 | `test_media_movel_tem_n_menos_janela_mais_um_resultados` | devolveu 2 resultados, não 3 | passou |
| 2 / #7 | `test_kahan_compensa_muitas_parcelas_de_decimo` | total `100000.00000133288`, erro `1.33e-6` | passou com total `100000.0` |
| 3 / #9 | `test_newton_recalcula_derivada_a_cada_iteracao` | derivada chamada uma única vez | passou com derivada recalculada |
| 4 / #11 | `test_integracao_tabela_irregular_linear` | trapézio devolveu 7, não 12 | passou com 12 |