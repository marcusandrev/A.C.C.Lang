# **CONTEXT FREE GRAMMAR**

| NO. | PRODUCTION |  | PRODUCTION SET |
| :---- | :---- | :---- | :---- |
| 1 | \<program\> | → | \<global-dec\> \<func-def\> shimenet kween ( ) { \<kween-body\> } \<func-def\> |
| 2 | \<global-dec\> | → | \<var-dec-init\> \<global-dec\> |
| 3 | \<global-dec\> | → | λ |
| 4 | \<var-dec-init\> | → | \<naur-case\> \<data-type\> \<var-init\> ;  |
| 5 | \<var-dec-init\> | → | \<data-type\> id \<func-array-init-tail\> ;  |
| 6 | \<var-dec-init\> | → | shimenet id \<func-case\> ; |
| 7 | \<var-dec-init\> | → | λ |
| 8 | \<naur-case\> | → | naur |
| 9 | \<naur-case\> | → | λ |
| 10 | \<return-type\> | → | \<data-type\> |
| 11 | \<return-type\> | → | shimenet |
| 12 | \<data-type\>  | → | anda |
| 13 | \<data-type\>  | → | andamhie |
| 14 | \<data-type\>  | → | chika |
| 15 | \<data-type\>  | → | eklabool |
| 16 | \<func-array-init-tail\> | → | \<func-case\> |
| 17 | \<func-array-init-tail\> | → | \<array-case\> \<array-init\> |
| 18 | \<func-case\> | → | ( \<parameters\> ) |
| 19 | \<parameters\> | → | \<func-parameters\> \<multi-parameters\> |
| 20 | \<parameters\> | → | λ  |
| 21 | \<func-parameters\> | → | \<data-type\> id  |
| 22 | \<multi-parameters\> | → | , \<func-parameters\> \<multi-parameters\> |
| 23 | \<multi-parameters\> | → | λ |
| 24 | \<array-case\> | → | \[ \<array-values\> \] \<2d-index\>  |
| 25 | \<array-case\> | → | λ |
| 26 | \<2d-index\> | → | \[ \<array-values\> \] \<3d-index\> |
| 27 | \<2d-index\> | → | λ |
| 28 | \<3d-index\>  | → | \[ \<array-values\> \] |
| 29 | \<3d-index\>  | → | λ |
| 30 | \<array-values\> | → | \<expression\> |
| 31 | \<literals\> | → | anda\_literal |
| 32 | \<literals\> | → | andamhie\_literal |
| 33 | \<literals\> | → | chika\_literal |
| 34 | \<literals\> | → | \<eklabool\> |
| 35 | \<eklabool\> | → | korik |
| 36 | \<eklabool\> | → | eme |
| 37 | \<func-array\>  | → | \<func-array-value\> |
| 38 | \<func-array\>   | → | λ |
| 39 | \<func-array-value\> | → | ( \<arguments\> ) |
| 40 | \<func-array-value\> | → | \<array-case\> |
| 41 | \<var-init\>  | → | id \<var-init-tail\> \<multi-init-values\> |
| 42 | \<var-init-tail\>  | → | \= \<init-values\> |
| 43 | \<var-init-tail\>  | → | λ |
| 44 | \<multi-init-values\> | → | , id \<multi-init-values-tail\> \<multi-init-values\> |
| 45 | \<multi-init-values\> | → | λ |
| 46 | \<multi-init-values-tail\> | → | \= \<init-values\>  |
| 47 | \<multi-init-values-tail\> | → | λ |
| 48 | \<init-values\> | → | \<expression\> |
| 49 | \<array-init\> | → | \= { \<array-elements\> } |
| 50 | \<array-elements\> | → | \<array-values\> \<extra-array-value\> |
| 51 | \<array-elements\> | → | { \<2d-array-elements\> } \<extra-2d-array-value\>  |
| 52 | \<2d-array-elements\> | → | \<array-values\> \<extra-array-value\> |
| 53 | \<2d-array-elements\> | → | { \<array-values\> \<extra-array-value\> } \<extra-2d-array-value\> |
| 54 | \<2d-array-elements\> | → | λ |
| 55 | \<extra-array-value\> | → | , \<array-values\> \<extra-array-value\> |
| 56 | \<extra-array-value\> | → | λ |
| 57 | \<extra-2d-array-value\> | → | , { \<extra-3d-array-value\> } \<extra-2d-array-value\> |
| 58 | \<extra-2d-array-value\> | → | λ |
| 59 | \<extra-3d-array-value\> | → | \<array-values\> \<extra-array-value\> |
| 60 | \<extra-3d-array-value\> | → | { \<array-values\> \<extra-array-value\> } \<extra-2d-array-value\> |
| 61 | \<extra-3d-array-value\> | → | λ |
| 62 | \<func-def\> | → | \<return-type\> id ( \<parameters\> ) { \<func-body\> } \<func-def\> |
| 63 | \<func-def\> | → | λ |
| 64 | \<func-body\> | → | \<local-dec\> \<statements\> \<multi-statements\> |
| 65 | \<func-body\> | → | λ |
| 66 | \<multi-statements\> | → | \<statements\> \<multi-statements\> |
| 67 | \<multi-statements\> | → | λ |
| 68 | \<local-dec\> | → | \<local-dec-init\> \<array-assign\> \<local-dec\> |
| 69 | \<local-dec\> | → | λ |
| 70 | \<local-dec-init\> | → | \<naur-case\> \<data-type\> \<var-init\> ;  |
| 71 | \<local-dec-init\> | → | \<data-type\> id \<array-case\> \<array-init\> ;  |
| 72 | \<arguments\> | → | \<arguments-value\> \<multi-arguments-value\> |
| 73 | \<arguments\> | → | λ |
| 74 | \<multi-arguments-value\> | → | , \<arguments-value\> \<multi-arguments-value\> |
| 75 | \<multi-arguments-value\> | → | λ |
| 76 | \<arguments-value\> | → | \<expression\> |
| 77 | \<array-assign\> | → | id \<array-case\> \= \<array-values\> ; |
| 78 | \<array-assign\> | → | λ |
| 79 | \<kween-body\> | → | \<func-body\> |
| 80 | \<expression\> | → | \<simple-expression\> |
| 81 | \<expression\> | → | \<multi-expression\> |
| 82 | \<simple-expression\> | → | \<expression-operands\> \<expression-tail\> |
| 83 | \<multi-expression\> | → | ( \<expression\> ) \<expression-tail\> |
| 84 | \<expression-tail\> | → | \<general-operators\> \<expression-operands\> \<expression-tail\> |
| 85 | \<expression-tail\> | → | λ |
| 86 | \<expression-operands\> | → | \<negative-value\> \<expression-value\> |
| 87 | \<negative-value\> | → | \- |
| 88 | \<negative-value\> | → | λ |
| 89 | \<expression-value\> | → | \<unary-operator\> id  |
| 90 | \<expression-value\> | → | id \<identifier-tail\> |
| 91 | \<expression-value\> | → | \<general-operands\> |
| 92 | \<expression-value\> | → | ( \<expression\> ) |
| 93 | \<identifier-tail\> | → | \<func-array\> |
| 94 | \<identifier-tail\> | → | \<unary-operator\> |
| 95 | \<identifier-tail\> | → | λ |
| 96 | \<unary-operator\> | → | \-- |
| 97 | \<unary-operator\> | → | \++ |
| 98 | \<general-operands\> | → | \<literals\> |
| 99 | \<general-operators\> | → | \+ |
| 100 | \<general-operators\> | → | \+= |
| 101 | \<general-operators\> | → | \- |
| 102 | \<general-operators\> | → | % |
| 103 | \<general-operators\> | → | / |
| 104 | \<general-operators\> | → | \*  |
| 105 | \<general-operators\> | → | \*\* |
| 106 | \<general-operators\> | → | // |
| 107 | \<general-operators\> | → | \>  |
| 108 | \<general-operators\> | → | \<  |
| 109 | \<general-operators\> | → | \>= |
| 110 | \<general-operators\> | → | \<= |
| 111 | \<general-operators\> | → | \== |
| 112 | \<general-operators\> | → | \!= |
| 113 | \<general-operators\> | → | \= |
| 114 | \<general-operators\> | → | && |
| 115 | \<general-operators\> | → | || |
| 116 | \<general-operators\> | → | \! |
| 117 | \<statements\> | → | id \<assign-stmts\> \<statements\> |
| 118 | \<statements\> | → | \<input-stmts\> \<statements\> |
| 119 | \<statements\> | → | \<output-stmts\> \<statements\> |
| 120 | \<statements\> | → | \<conditional-stmts\> \<statements\> |
| 121 | \<statements\> | → | \<loop-stmts\> \<statements\> |
| 122 | \<statements\> | → | \<switch-stmts\> \<statements\> |
| 123 | \<statements\> | → | \<control-flow-stmts\> \<statements\> |
| 124 | \<statements\> | → | \<return-stmts\> \<statements\> |
| 125 | \<statements\> | → | \<unary-stmts\> \<statements\> |
| 126 | \<statements\> | → | λ |
| 127 | \<assign-stmts\> | → | \<func-array\> \<arithmetic-operators\> \= \<assignment-values\> ; |
| 128 | \<arithmetic-operators\> | → | \+ |
| 129 | \<arithmetic-operators\> | → | \- |
| 130 | \<arithmetic-operators\> | → | % |
| 131 | \<arithmetic-operators\> | → | / |
| 132 | \<arithmetic-operators\> | → | // |
| 133 | \<arithmetic-operators\> | → | \* |
| 134 | \<arithmetic-operators\> | → | \*\* |
| 135 | \<arithmetic-operators\> | → | λ |
| 136 | \<assignment-values\> | → | \<expression\> |
| 137 | \<input-stmts\> | → | \<input-type\> id \= givenchy ( \<givenchy-values\> ) ; |
| 138 | \<input-type\> | → | \<data-type\> |
| 139 | \<input-type\> | → | λ |
| 140 | \<givenchy-values\> | → | \<expression-operands\> |
| 141 | \<output-stmts\> | → | serve ( \<output-values\> ) ; |
| 142 | \<output-values\> | → | \<expression\> |
| 143 | \<conditional-stmts\> | → | pak ( \<condition\> ) { \<conditional-body\> } \<ganern-pak-statement\> \<ganern-case\> |
| 144 | \<condition\> | → | \<expression\> |
| 145 | \<conditional-body\> | → | \<local-dec\> \<statements\> \<multi-statements\> |
| 146 | \<conditional-body\> | → | λ |
| 147 | \<ganern-pak-statement\> | → | ganern pak ( \<condition\> ) { \<conditional-body\> } \<ganern-pak-statement\> |
| 148 | \<ganern-pak-statement\> | → | λ |
| 149 | \<ganern-case\> | → | ganern { \<conditional-body\> } |
| 150 | \<ganern-case\> | → | λ |
| 151 | \<loop-stmts\> | → | \<forda-statement\> |
| 152 | \<loop-stmts\> | → | \<keri-statement\> |
| 153 | \<forda-statement\> | → | forda ( \<loop-type-init\> id from \<start-value\> to \<end-value\> \<step-case\> ) { \<for-loop-body\> } |
| 154 | \<loop-type-init\> | → | \<data-type\> |
| 155 | \<loop-type-init\> | → | λ |
| 156 | \<start-value\> | → | \<loop-conditions\> |
| 157 | \<end-value\> | → | \<loop-conditions\> |
| 158 | \<step-case\> | → | step \<update\> |
| 159 | \<step-case\> | → | λ |
| 160 | \<update\> | → | \<expression\> |
| 161 | \<update\> | → | λ |
| 162 | \<loop-conditions\> | → | \<expression\> |
| 163 | \<for-loop-body\> | → | \<local-dec\> \<statements\> \<multi-statements\> |
| 164 | \<for-loop-body\> | → | λ |
| 165 | \<keri-statement\> | → | keri \<keri-case\>  |
| 166 | \<keri-case\> | → | ( \<condition\> ) { \<while-loop-body\> } |
| 167 | \<keri-case\> | → | lang { \<while-loop-body\> } keri ( \<condition\> ) |
| 168 | \<while-loop-body\> | → | \<local-dec\> \<statements\> \<multi-statements\> |
| 169 | \<while-loop-body\> | → | λ |
| 170 | \<switch-stmts\> | → | versa ( \<switch-values\> ) { betsung \<switch-values\> : \<switch-statements\> \<amaccana-case\> \<multi-cases\> \<ditech-case\> } |
| 171 | \<multi-cases\> | → | betsung \<switch-values\> : \<switch-statements\> \<amaccana-case\> \<multi-cases\> |
| 172 | \<multi-cases\> | → | λ |
| 173 | \<switch-values\> | → | \<expression\> |
| 174 | \<switch-statements\> | → | \<local-dec\> \<statements\> \<multi-statements\> |
| 175 | \<amaccana-case\> | → | amaccana ; |
| 176 | \<amaccana-case\> | → | λ |
| 177 | \<ditech-case\> | → | ditech : \<switch-statements\> |
| 178 | \<ditech-case\> | → | λ |
| 179 | \<control-flow-stmts\> | → | gogogo ; |
| 180 | \<control-flow-stmts\> | → | amaccana ; |
| 181 | \<return-stmts\> | → | push \<push-values\> ;    |
| 182 | \<return-stmts\> | → | λ |
| 183 | \<unary-stmts\> | → | \<unary-operator\> id ; |
| 184 | \<unary-stmts\> | → | id \<unary-operator\> ; |
| 185 | \<push-values\> | → | \<expression\> |
| 186 | \<push-values\> | → | λ |

