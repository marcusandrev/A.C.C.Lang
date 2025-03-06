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
| 50 | \<array-init\> | → | λ |
| 51 | \<array-elements\> | → | \<array-values\> \<extra-array-value\> |
| 52 | \<array-elements\> | → | { \<2d-array-elements\> } \<extra-2d-array-value\>  |
| 53 | \<2d-array-elements\> | → | \<array-values\> \<extra-array-value\> |
| 54 | \<2d-array-elements\> | → | { \<array-values\> \<extra-array-value\> } \<extra-2d-array-value\> |
| 55 | \<2d-array-elements\> | → | λ |
| 56 | \<extra-array-value\> | → | , \<array-values\> \<extra-array-value\> |
| 57 | \<extra-array-value\> | → | λ |
| 58 | \<extra-2d-array-value\> | → | , { \<extra-3d-array-value\> } \<extra-2d-array-value\> |
| 59 | \<extra-2d-array-value\> | → | λ |
| 60 | \<extra-3d-array-value\> | → | \<array-values\> \<extra-array-value\> |
| 61 | \<extra-3d-array-value\> | → | { \<array-values\> \<extra-array-value\> } \<extra-2d-array-value\> |
| 62 | \<extra-3d-array-value\> | → | λ |
| 63 | \<func-def\> | → | \<return-type\> id ( \<parameters\> ) { \<func-body\> } \<func-def\> |
| 64 | \<func-def\> | → | λ |
| 65 | \<func-body\> | → | \<local-dec\> \<statements\> \<multi-statements\> |
| 66 | \<func-body\> | → | λ |
| 67 | \<multi-statements\> | → | \<statements\> \<multi-statements\> |
| 68 | \<multi-statements\> | → | λ |
| 69 | \<local-dec\> | → | \<local-dec-init\> \<array-assign\> \<local-dec\> |
| 70 | \<local-dec\> | → | λ |
| 71 | \<local-dec-init\> | → | \<naur-case\> \<data-type\> \<var-init\> ;  |
| 72 | \<local-dec-init\> | → | \<data-type\> id \<array-case\> \<array-init\> ;  |
| 73 | \<arguments\> | → | \<arguments-value\> \<multi-arguments-value\> |
| 74 | \<arguments\> | → | λ |
| 75 | \<multi-arguments-value\> | → | , \<arguments-value\> \<multi-arguments-value\> |
| 76 | \<multi-arguments-value\> | → | λ |
| 77 | \<arguments-value\> | → | \<expression\> |
| 78 | \<array-assign\> | → | id \<array-case\> \= \<array-values\> ; |
| 79 | \<array-assign\> | → | λ |
| 80 | \<kween-body\> | → | \<func-body\> |
| 81 | \<expression\> | → | \<simple-expression\> |
| 82 | \<expression\> | → | \<multi-expression\> |
| 83 | \<simple-expression\> | → | \<expression-operands\> \<expression-tail\> |
| 84 | \<multi-expression\> | → | ( \<expression\> ) \<expression-tail\> |
| 85 | \<expression-tail\> | → | \<general-operators\> \<expression-operands\> \<expression-tail\> |
| 86 | \<expression-tail\> | → | λ |
| 87 | \<expression-operands\> | → | \<negative-not-value\> \<expression-value\> |
| 88 | \<negative-not-value\> | → | \- |
| 89 | \<negative-not-value\> | → | \! |
| 90 | \<negative-not-value\> | → | λ |
| 91 | \<expression-value\> | → | \<unary-operator\> id  |
| 92 | \<expression-value\> | → | id \<identifier-tail\> |
| 93 | \<expression-value\> | → | \<general-operands\> |
| 94 | \<expression-value\> | → | ( \<expression\> ) |
| 95 | \<identifier-tail\> | → | \<func-array\> |
| 96 | \<identifier-tail\> | → | \<unary-operator\> |
| 97 | \<identifier-tail\> | → | λ |
| 98 | \<unary-operator\> | → | \-- |
| 99 | \<unary-operator\> | → | \++ |
| 100 | \<general-operands\> | → | \<literals\> |
| 101 | \<general-operators\> | → | \+ |
| 102 | \<general-operators\> | → | \- |
| 103 | \<general-operators\> | → | % |
| 104 | \<general-operators\> | → | / |
| 105 | \<general-operators\> | → | \*  |
| 106 | \<general-operators\> | → | \*\* |
| 107 | \<general-operators\> | → | // |
| 108 | \<general-operators\> | → | \>  |
| 109 | \<general-operators\> | → | \<  |
| 110 | \<general-operators\> | → | \>= |
| 111 | \<general-operators\> | → | \<= |
| 112 | \<general-operators\> | → | \== |
| 113 | \<general-operators\> | → | \!= |
| 114 | \<general-operators\> | → | \= |
| 115 | \<general-operators\> | → | && |
| 116 | \<general-operators\> | → | || |
| 117 | \<statements\> | → | id \<assign-stmts\> \<statements\> |
| 118 | \<statements\> | → | \<input-stmts\> \<statements\> |
| 119 | \<statements\> | → | \<output-stmts\> \<statements\> |
| 120 | \<statements\> | → | \<conditional-stmts\> \<statements\> |
| 121 | \<statements\> | → | \<loop-stmts\> \<statements\> |
| 122 | \<statements\> | → | \<switch-stmts\> \<statements\> |
| 123 | \<statements\> | → | \<return-stmts\> \<statements\> |
| 124 | \<statements\> | → | \<unary-stmts\> \<statements\> |
| 125 | \<statements\> | → | λ |
| 126 | \<loop-body\> | → | id \<assign-stmts\> \<loop-body\> |
| 127 | \<loop-body\> | → | \<input-stmts\> \<loop-body\> |
| 128 | \<loop-body\> | → | \<output-stmts\> \<loop-body\> |
| 129 | \<loop-body\> | → | \<loop-stmts\> \<loop-body\> |
| 130 | \<loop-body\> | → | \<loop-conditional-stmts\> \<loop-body\> |
| 131 | \<loop-body\> | → | \<loop-switch-stmts\> \<loop-body\> |
| 132 | \<loop-body\> | → | \<return-stmts\> \<loop-body\> |
| 133 | \<loop-body\> | → | \<unary-stmts\> \<loop-body\> |
| 134 | \<loop-body\> | → | \<control-flow-stmts\> \<loop-body\> |
| 135 | \<loop-body\> | → | λ |
| 136 | \<multi-loop-body\> | → | \<loop-body\> \<multi-loop-body\> |
| 137 | \<multi-loop-body\> | → | λ |
| 138 | \<assign-stmts\> | → | \<func-array\> \<assignment-operators\> \<assignment-values\> ; |
| 139 | \<assignment-operators\> | → | \= |
| 140 | \<assignment-operators\> | → | \+= |
| 141 | \<assignment-operators\> | → | \-= |
| 142 | \<assignment-operators\> | → | %= |
| 143 | \<assignment-operators\> | → | /= |
| 144 | \<assignment-operators\> | → | //= |
| 145 | \<assignment-operators\> | → | \*= |
| 146 | \<assignment-operators\> | → | \*\*= |
| 147 | \<assignment-values\> | → | \<expression\> |
| 148 | \<input-stmts\> | → | \<input-type\> id \= givenchy ( \<givenchy-values\> ) ; |
| 149 | \<input-type\> | → | \<data-type\> |
| 150 | \<input-type\> | → | λ |
| 151 | \<givenchy-values\> | → | \<expression-operands\> |
| 152 | \<output-stmts\> | → | serve ( \<output-values\> ) ; |
| 153 | \<output-values\> | → | \<expression\> |
| 154 | \<conditional-stmts\> | → | pak ( \<condition\> ) { \<conditional-body\> } \<ganern-pak-statement\> \<ganern-case\> |
| 155 | \<condition\> | → | \<expression\> |
| 156 | \<conditional-body\> | → | \<local-dec\> \<statements\> \<multi-statements\> |
| 157 | \<conditional-body\> | → | λ |
| 158 | \<loop-conditional-stmts\> | → | pak ( \<condition\> ) { \<loop-conditional-body\> } \<ganern-pak-statement\> \<ganern-case\> |
| 159 | \<loop-conditional-body\> | → | \<local-dec\> \<loop-body\> \<multi-loop-body\> |
| 160 | \<loop-conditional-body\> | → | λ |
| 161 | \<ganern-pak-statement\> | → | ganern pak ( \<condition\> ) { \<conditional-body\> } \<ganern-pak-statement\> |
| 162 | \<ganern-pak-statement\> | → | λ |
| 163 | \<ganern-case\> | → | ganern { \<conditional-body\> } |
| 164 | \<ganern-case\> | → | λ |
| 165 | \<loop-stmts\> | → | \<forda-statement\> |
| 166 | \<loop-stmts\> | → | \<keri-statement\> |
| 167 | \<forda-statement\> | → | forda ( \<loop-type-init\> id from \<start-value\> to \<end-value\> \<step-case\> ) { \<for-loop-body\> } |
| 168 | \<loop-type-init\> | → | \<data-type\> |
| 169 | \<loop-type-init\> | → | λ |
| 170 | \<start-value\> | → | \<loop-conditions\> |
| 171 | \<end-value\> | → | \<loop-conditions\> |
| 172 | \<step-case\> | → | step \<update\> |
| 173 | \<step-case\> | → | λ |
| 174 | \<update\> | → | \<expression\> |
| 175 | \<update\> | → | λ |
| 176 | \<loop-conditions\> | → | \<expression\> |
| 177 | \<for-loop-body\> | → | \<local-dec\> \<loop-body\> \<multi-loop-body\> |
| 178 | \<for-loop-body\> | → | λ |
| 179 | \<keri-statement\> | → | keri \<keri-case\>  |
| 180 | \<keri-case\> | → | ( \<condition\> ) { \<while-loop-body\> } |
| 181 | \<keri-case\> | → | lang { \<while-loop-body\> } keri ( \<condition\> ) |
| 182 | \<while-loop-body\> | → | \<local-dec\> \<loop-body\> \<multi-loop-body\> |
| 183 | \<while-loop-body\> | → | λ |
| 184 | \<switch-stmts\> | → | versa ( \<switch-values\> ) { betsung \<switch-values\> : \<switch-statements\> \<amaccana-case\> \<multi-cases\> \<ditech-case\> } |
| 185 | \<multi-cases\> | → | betsung \<switch-values\> : \<switch-statements\> \<amaccana-case\> \<multi-cases\> |
| 186 | \<multi-cases\> | → | λ |
| 187 | \<switch-values\> | → | \<expression\> |
| 188 | \<switch-statements\> | → | \<local-dec\> \<statements\> \<multi-statements\> |
| 189 | \<loop-switch-stmts\> | → | versa ( \<switch-values\> ) { betsung \<switch-values\> : \<loop-switch-statements\> \<loop-multi-cases\> \<ditech-case\> } |
| 190 | \<loop-multi-cases\> | → | betsung \<switch-values\> : \<loop-switch-statements\> \<loop-multi-cases\> |
| 191 | \<loop-multi-cases\> | → | λ |
| 192 | \<loop-switch-statements\> | → | \<local-dec\> \<loop-body\> \<multi-loop-body\> |
| 193 | \<amaccana-case\> | → | amaccana ; |
| 194 | \<amaccana-case\> | → | λ |
| 195 | \<ditech-case\> | → | ditech : \<switch-statements\> |
| 196 | \<ditech-case\> | → | λ |
| 197 | \<control-flow-stmts\> | → | gogogo ; |
| 198 | \<control-flow-stmts\> | → | amaccana ; |
| 199 | \<control-flow-stmts\> | → | λ |
| 200 | \<return-stmts\> | → | push \<push-values\> ;    |
| 201 | \<return-stmts\> | → | λ |
| 202 | \<unary-stmts\> | → | \<unary-operator\> id ; |
| 203 | \<unary-stmts\> | → | id \<unary-operator\> ; |
| 204 | \<push-values\> | → | \<expression\> |
| 205 | \<push-values\> | → | λ |

