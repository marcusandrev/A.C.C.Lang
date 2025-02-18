# **CONTEXT FREE GRAMMAR**

| NO. | PRODUCTION |  | PRODUCTION SET |
| :---- | :---- | :---- | :---- |
| 1 | \<program\> | → | \<global-dec\> \<func-def\> shimenet kween ( ) { \<kween-body\> } \<func-def\> |
| 2 | \<global-dec\> | → | \<var-dec-init\> \<global-dec\> |
| 3 | \<global-dec\> | → | λ |
| 4 | \<var-dec-init\> | → | \<naur-case\> \<data-type\> id \<var-dec-init-tail\> ; |
| 5 | \<var-dec-init\> | → | λ |
| 6 | \<naur-case\> | → | naur |
| 7 | \<naur-case\> | → | λ |
| 8 | \<return-type\> | → | \<data-type\> |
| 9 | \<return-type\> | → | shimenet |
| 10 | \<data-type\>  | → | anda |
| 11 | \<data-type\>  | → | andamhie |
| 12 | \<data-type\>  | → | chika |
| 13 | \<data-type\>  | → | eklabool |
| 14 | \<var-dec-init-tail\> | → | \<func-case\> |
| 15 | \<var-dec-init-tail\> | → | \<array-case\> \<var-init\> |
| 16 | \<var-dec-init-tail\> | → | λ |
| 17 | \<func-case\> | → | ( \<arguments\> ) |
| 18 | \<arguments\> | → | \<func-arguments\> \<multi-arguments\> |
| 19 | \<arguments\> | → | λ |
| 20 | \<func-arguments\> | → | \<argument-type\> id  |
| 21 | \<argument-type\> | → | \<data-type\> |
| 22 | \<argument-type\> | → | λ |
| 23 | \<multi-arguments\> | → | , \<func-arguments\> \<multi-arguments\> |
| 24 | \<multi-arguments\> | → | λ |
| 25 | \<array-case\> | → | \[ \<array-values\> \] \<2d-index\>  |
| 26 | \<array-case\> | → | λ |
| 27 | \<2d-index\> | → | \[ \<array-values\> \] \<3d-index\> |
| 28 | \<2d-index\> | → | λ |
| 29 | \<3d-index\>  | → | \[ \<array-values\> \] |
| 30 | \<3d-index\>  | → | λ |
| 31 | \<array-values\> | → | \<expression-operands\> |
| 32 | \<literals\> | → | anda\_literal |
| 33 | \<literals\> | → | andamhie\_literal |
| 34 | \<literals\> | → | chika\_literal |
| 35 | \<literals\> | → | \<eklabool\> |
| 36 | \<eklabool\> | → | korik |
| 37 | \<eklabool\> | → | eme |
| 38 | \<func-array\>  | → | \<func-array-value\> |
| 39 | \<func-array\>   | → | λ |
| 40 | \<func-array-value\> | → | ( \<arguments\> ) |
| 41 | \<func-array-value\> | → | \<array-case\> |
| 42 | \<var-init\>  | → | \= \<init-values\> \<multi-init-values\>  |
| 43 | \<var-init\>  | → | λ |
| 44 | \<multi-init-values\> | → | , id \<array-case\> \= \<init-values\> \<multi-init-values\>  |
| 45 | \<multi-init-values\> | → | λ |
| 46 | \<init-values\> | → | { \<array-elements\> } |
| 47 | \<init-values\> | → | \<expression\> |
| 48 | \<array-elements\> | → | \<array-values\> \<extra-array-value\> |
| 49 | \<array-elements\> | → | { \<2d-array-elements\> } \<extra-2d-array-value\>  |
| 50 | \<2d-array-elements\> | → | \<array-values\> \<extra-array-value\> |
| 51 | \<2d-array-elements\> | → | { \<array-values\> \<extra-array-value\> } \<extra-2d-array-value\> |
| 52 | \<2d-array-elements\> | → | λ |
| 53 | \<extra-array-value\> | → | , \<array-values\> \<extra-array-value\> |
| 54 | \<extra-array-value\> | → | λ |
| 55 | \<extra-2d-array-value\> | → | , { \<extra-3d-array-value\> } \<extra-2d-array-value\> |
| 56 | \<extra-2d-array-value\> | → | λ |
| 57 | \<extra-3d-array-value\> | → | \<array-values\> \<extra-array-value\> |
| 58 | \<extra-3d-array-value\> | → | { \<array-values\> \<extra-array-value\> } \<extra-2d-array-value\> |
| 59 | \<extra-3d-array-value\> | → | λ |
| 62 | \<func-def\> | → | \<return-type\> id ( \<parameters\> ) { \<func-body\> } \<func-def\> |
| 63 | \<func-def\> | → | λ |
| 64 | \<parameters\> | → | \<arguments\> |
| 65 | \<func-body\> | → | \<local-dec\> \<statements\> \<multi-statements\> |
| 66 | \<local-dec\> | → | \<var-dec-init\> \<array-assign\> \<local-dec\> |
| 67 | \<local-dec\> | → | λ |
| 68 | \<func-assign\> | → | id \= \<func-call\> |
| 69 | \<func-call\> | → | id ( \<arguments\> ) |
| 70 | \<array-assign\> | → | id \<array-case\> \= \<array-values\> ; |
| 71 | \<array-assign\> | → | λ |
| 72 | \<kween-body\> | → | \<func-body\> |
| 73 | \<expression\> | → | \<simple-expression\> |
| 74 | \<expression\> | → | \<multi-expression\> |
| 75 | \<simple-expression\> | → | \<expression-operands\> \<expression-tail\> |
| 76 | \<multi-expression\> | → | ( \<expression\> ) \<more-expression\> |
| 77 | \<more-expression\> | → | \<general-operators\> \<expression-operands\> \<more-expression\> |
| 78 | \<more-expression\> | → | λ |
| 79 | \<expression-tail\> | → | \<general-operators\> \<expression-operands\> \<more-expression\> |
| 80 | \<expression-tail\> | → | λ |
| 81 | \<expression-operands\> | → | \<negative-value\> \<expression-value\> |
| 82 | \<negative-value\> | → | \- |
| 83 | \<negative-value\> | → | λ |
| 84 | \<expression-value\> | → | \<unary-operator\> id  |
| 85 | \<expression-value\> | → | id \<identifier-tail\> |
| 86 | \<expression-value\> | → | \<general-operands\> |
| 87 | \<identifier-tail\> | → | \<func-array\> |
| 88 | \<identifier-tail\> | → | \<unary-operator\> |
| 90 | \<identifier-tail\> | → | λ |
| 91 | \<unary-operator\> | → | \-- |
| 92 | \<unary-operator\> | → | \++ |
| 93 | \<general-operands\> | → | \<literals\> |
| 94 | \<general-operators\> | → | \+ |
| 95 | \<general-operators\> | → | \+= |
| 96 | \<general-operators\> | → | \- |
| 98 | \<general-operators\> | → | % |
| 99 | \<general-operators\> | → | / |
| 100 | \<general-operators\> | → | \*  |
| 101 | \<general-operators\> | → | \*\* |
| 102 | \<general-operators\> | → | // |
| 101 | \<general-operators\> | → | \>  |
| 102 | \<general-operators\> | → | \<  |
| 104 | \<general-operators\> | → | \>= |
| 105 | \<general-operators\> | → | \<= |
| 106 | \<general-operators\> | → | \== |
| 107 | \<general-operators\> | → | \!= |
| 112 | \<general-operators\> | → | \= |
| 113 | \<general-operators\> | → | && |
| 114 | \<general-operators\> | → | || |
| 115 | \<general-operators\> | → | \! |
| 116 | \<statements\> | → | \<assign-stmts\> \<statements\> |
| 117 | \<statements\> | → | \<input-stmts\> \<statements\> |
| 118 | \<statements\> | → | \<output-stmts\> \<statements\> |
| 119 | \<statements\> | → | \<conditional-stmts\> \<statements\> |
| 120 | \<statements\> | → | \<loop-stmts\> \<statements\> |
| 121 | \<statements\> | → | \<switch-stmts\> \<statements\> |
| 122 | \<statements\> | → | \<control-flow-stmts\> \<statements\> |
| 123 | \<statements\> | → | \<return-stmts\> \<statements\> |
| 124 | \<statements\> | → | λ |
| 125 | \<assign-stmts\> | → | id \<arithmetic-operators\> \= \<assignment-values\> ; |
| 126 | \<arithmetic-operators\> | → | \+ |
| 127 | \<arithmetic-operators\> | → | \- |
| 128 | \<arithmetic-operators\> | → | % |
| 129 | \<arithmetic-operators\> | → | / |
| 130 | \<arithmetic-operators\> | → | // |
| 131 | \<arithmetic-operators\> | → | \* |
| 132 | \<arithmetic-operators\> | → | \*\* |
| 133 | \<assignment-values\> | → | \<expression-operands\> |
| 134 | \<input-stmts\> | → | \<input-type\> id \= givenchy ( \<givenchy-values\> ) ; |
| 135 | \<input-type\> | → | \<data-type\> |
| 136 | \<input-type\> | → | λ |
| 137 | \<givenchy-values\> | → | \<expression-operands\> |
| 138 | \<output-stmts\> | → | serve ( \<output-values\> ) ; |
| 139 | \<output-values\> | → | \<expression-operands\> |
| 140 | \<conditional-stmts\> | → | pak ( \<condition\> ) { \<conditional-body\> } \<ganern-pak-statement\> \<ganern-case\> |
| 141 | \<condition\> | → | \<expression-operands\> |
| 142 | \<conditional-body\> | → | \<local-dec\> \<statements\> \<multi-statements\> |
| 143 | \<ganern-pak-statement\> | → | ganern pak ( \<condition\> ) { \<conditional-body\> } \<ganern-pak-statement\> |
| 144 | \<ganern-pak-statement\> | → | λ |
| 145 | \<ganern-case\> | → | ganern { \<conditional-body\> } |
| 146 | \<ganern-case\> | → | λ |
| 147 | \<loop-stmts\> | → | \<forda-statement\> |
| 148 | \<loop-stmts\> | → | \<keri-statement\> |
| 149 | \<forda-statement\> | → | forda ( \<loop-type-init\> id from \<start-value\> to \<end-value\> \<step-case\> ) { \<for-loop-body\> } |
| 150 | \<loop-type-init\> | → | \<data-type\> |
| 151 | \<loop-type-init\> | → | λ |
| 152 | \<start-value\> | → | \<loop-conditions\> |
| 153 | \<end-value\> | → | \<loop-conditions\> |
| 154 | \<step-case\> | → | step \<update\> |
| 155 | \<step-case\> | → | λ |
| 156 | \<loop-conditions\> | → | \<expression-operands\> |
| 157 |  \<for-loop-body\> | → | \<local-dec\> \<statements\> \<multi-statements\> |
| 158 | \<keri-statement\> | → | keri \<keri-case\>  |
| 159 | \<keri-case\> | → | ( \<condition\> ) { \<while-loop-body\> } |
| 160 | \<keri-case\> | → | lang { \<while-loop-body\> } keri ( \<condition\> ) ; |
| 161 | \<while-loop-body\> | → | \<local-dec\> \<statements\> \<multi-statements\> |
| 162 | \<switch-stmts\> | → | versa ( \<switch-values\> ) {betsung \<switch-values\> : \<switch-statements\> \<amaccana-case\> ; \<multi-cases\> \<ditech-case\> \<switch-statements\> } |
| 163 | \<multi-cases\> | → | betsung \<switch-values\> : \<switch-statements\> \<amaccana-case\> ; \<multi-cases\> |
| 164 | \<multi-cases\> | → | λ |
| 165 | \<switch-values\> | → | \<expression-operands\> |
| 166 | \<switch-statements\> | → | \<local-dec\> \<statements\> \<multi-statements\> |
| 167 | \<amaccana-case\> | → | amaccana |
| 168 | \<amaccana-case\> | → | λ |
| 169 | \<ditech-case\> | → | ditech : |
| 170 | \<ditech-case\> | → | λ |
| 171 | \<control-flow-stmts\> | → | gogogo ; |
| 172 | \<control-flow-stmts\> | → | amaccana ; |
| 173 | \<return-stmts\> | → | push \<push-values\> ;    |
| 174 | \<return-stmts\> | → | λ |
| 175 | \<push-values\> | → | \<expression\> |
| 176 | \<push-values\> | → | λ |