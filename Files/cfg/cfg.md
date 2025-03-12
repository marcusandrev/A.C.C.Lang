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
| 65 | \<func-body\> | → | \<local-dec\> \<statements\>  |
| 66 | \<func-body\> | → | λ |
| 67 | \<local-dec\> | → | \<local-dec-init\> \<array-assign\> \<local-dec\> |
| 68 | \<local-dec\> | → | λ |
| 69 | \<local-dec-init\> | → | \<naur-case\> \<data-type\> \<var-init\> ;  |
| 70 | \<local-dec-init\> | → | \<data-type\> id \<array-case\> \<array-init\> ;  |
| 71 | \<arguments\> | → | \<arguments-value\> \<multi-arguments-value\> |
| 72 | \<arguments\> | → | λ |
| 73 | \<multi-arguments-value\> | → | , \<arguments-value\> \<multi-arguments-value\> |
| 74 | \<multi-arguments-value\> | → | λ |
| 75 | \<arguments-value\> | → | \<expression\> |
| 76 | \<array-assign\> | → | id \<array-case\> \= \<array-values\> ; |
| 77 | \<array-assign\> | → | λ |
| 78 | \<kween-body\> | → | \<func-body\> |
| 79 | \<expression\> | → | \<simple-expression\> |
| 80 | \<expression\> | → | \<multi-expression\> |
| 81 | \<simple-expression\> | → | \<expression-operands\> \<expression-tail\> |
| 82 | \<multi-expression\> | → | ( \<expression\> ) \<expression-tail\> |
| 83 | \<expression-tail\> | → | \<general-operators\> \<expression-operands\> \<expression-tail\> |
| 84 | \<expression-tail\> | → | λ |
| 85 | \<expression-operands\> | → | \<negative-not-value\> \<expression-value\> |
| 86 | \<negative-not-value\> | → | \- |
| 87 | \<negative-not-value\> | → | \! |
| 88 | \<negative-not-value\> | → | λ |
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
| 100 | \<general-operators\> | → | \- |
| 101 | \<general-operators\> | → | % |
| 102 | \<general-operators\> | → | / |
| 103 | \<general-operators\> | → | \*  |
| 104 | \<general-operators\> | → | \*\* |
| 105 | \<general-operators\> | → | // |
| 106 | \<general-operators\> | → | \>  |
| 107 | \<general-operators\> | → | \<  |
| 108 | \<general-operators\> | → | \>= |
| 109 | \<general-operators\> | → | \<= |
| 110 | \<general-operators\> | → | \== |
| 111 | \<general-operators\> | → | \!= |
| 112 | \<general-operators\> | → | && |
| 113 | \<general-operators\> | → | || |
| 115 | \<statements\> | → | id \<assign-call-stmts\> \<statements\> |
| 116 | \<statements\> | → | \<input-stmts\> \<statements\> |
| 117 | \<statements\> | → | \<output-stmts\> \<statements\> |
| 118 | \<statements\> | → | \<conditional-stmts\> \<statements\> |
| 119 | \<statements\> | → | \<loop-stmts\> \<statements\> |
| 120 | \<statements\> | → | \<switch-stmts\> \<statements\> |
| 121 | \<statements\> | → | \<return-stmts\> \<statements\> |
| 122 | \<statements\> | → | \<unary-stmts\> \<statements\> |
| 123 | \<statements\> | → | λ |
| 124 | \<loop-body\> | → | id \<assign-call-stmts\> \<statements\> |
| 125 | \<loop-body\> | → | \<input-stmts\> \<loop-body\> |
| 126 | \<loop-body\> | → | \<output-stmts\> \<loop-body\> |
| 127 | \<loop-body\> | → | \<loop-stmts\> \<loop-body\> |
| 128 | \<loop-body\> | → | \<loop-conditional-stmts\> \<loop-body\> |
| 129 | \<loop-body\> | → | \<loop-switch-stmts\> \<loop-body\> |
| 130 | \<loop-body\> | → | \<return-stmts\> \<loop-body\> |
| 131 | \<loop-body\> | → | \<unary-stmts\> \<loop-body\> |
| 132 | \<loop-body\> | → | \<control-flow-stmts\> \<loop-body\> |
| 133 | \<loop-body\> | → | λ |
| 134 | \<multi-loop-body\> | → | \<loop-body\> \<multi-loop-body\> |
| 135 | \<multi-loop-body\> | → | λ |
| 136 | \<assign-call-stmts\> | → | \<array-case\> \<assignment-operators\> \<assignment-values\> ; |
| 137 | \<assign-call-stmts\> | → | ( \<arguments\> ) ; |
| 138 | \<assignment-operators\> | → | \= |
| 139 | \<assignment-operators\> | → | \+= |
| 140 | \<assignment-operators\> | → | \-= |
| 141 | \<assignment-operators\> | → | %= |
| 142 | \<assignment-operators\> | → | /= |
| 143 | \<assignment-operators\> | → | //= |
| 144 | \<assignment-operators\> | → | \*= |
| 145 | \<assignment-operators\> | → | \*\*= |
| 146 | \<assignment-values\> | → | \<expression\> |
| 147 | \<input-stmts\> | → | \<input-type\> id \= givenchy ( \<givenchy-values\> ) ; |
| 148 | \<input-type\> | → | \<data-type\> |
| 149 | \<input-type\> | → | λ |
| 150 | \<givenchy-values\> | → | \<expression-operands\> |
| 151 | \<output-stmts\> | → | serve ( \<output-values\> ) ; |
| 152 | \<output-values\> | → | \<expression\> |
| 153 | \<conditional-stmts\> | → | pak ( \<condition\> ) { \<conditional-body\> } \<ganern-pak-statement\> \<ganern-case\> |
| 154 | \<condition\> | → | \<expression\> |
| 155 | \<conditional-body\> | → | \<local-dec\> \<statements\>  |
| 156 | \<conditional-body\> | → | λ |
| 157 | \<loop-conditional-stmts\> | → | pak ( \<condition\> ) { \<loop-conditional-body\> } \<ganern-pak-statement\> \<ganern-case\> |
| 158 | \<loop-conditional-body\> | → | \<local-dec\> \<loop-body\> \<multi-loop-body\> |
| 159 | \<loop-conditional-body\> | → | λ |
| 160 | \<ganern-pak-statement\> | → | ganern pak ( \<condition\> ) { \<conditional-body\> } \<ganern-pak-statement\> |
| 161 | \<ganern-pak-statement\> | → | λ |
| 162 | \<ganern-case\> | → | ganern { \<conditional-body\> } |
| 163 | \<ganern-case\> | → | λ |
| 164 | \<loop-stmts\> | → | \<forda-statement\> |
| 165 | \<loop-stmts\> | → | \<keri-statement\> |
| 166 | \<forda-statement\> | → | forda ( \<loop-type-init\> id from \<start-value\> to \<end-value\> \<step-case\> ) { \<for-loop-body\> } |
| 167 | \<loop-type-init\> | → | \<data-type\> |
| 168 | \<loop-type-init\> | → | λ |
| 169 | \<start-value\> | → | \<loop-conditions\> |
| 170 | \<end-value\> | → | \<loop-conditions\> |
| 171 | \<step-case\> | → | step \<update\> |
| 172 | \<step-case\> | → | λ |
| 173 | \<update\> | → | \<expression\> |
| 174 | \<update\> | → | λ |
| 175 | \<loop-conditions\> | → | \<expression\> |
| 176 | \<for-loop-body\> | → | \<local-dec\> \<loop-body\> \<multi-loop-body\> |
| 177 | \<for-loop-body\> | → | λ |
| 178 | \<keri-statement\> | → | keri \<keri-case\>  |
| 179 | \<keri-case\> | → | ( \<condition\> ) { \<while-loop-body\> } |
| 180 | \<keri-case\> | → | lang { \<while-loop-body\> } keri ( \<condition\> ) |
| 181 | \<while-loop-body\> | → | \<local-dec\> \<loop-body\> \<multi-loop-body\> |
| 182 | \<while-loop-body\> | → | λ |
| 183 | \<switch-stmts\> | → | versa ( \<switch-values\> ) { betsung \<switch-values\> : \<switch-statements\> \<amaccana-case\> \<multi-cases\> \<ditech-case\> } |
| 184 | \<multi-cases\> | → | betsung \<switch-values\> : \<switch-statements\> \<amaccana-case\> \<multi-cases\> |
| 185 | \<multi-cases\> | → | λ |
| 186 | \<switch-values\> | → | \<expression\> |
| 187 | \<switch-statements\> | → | \<local-dec\> \<statements\>  |
| 188 | \<loop-switch-stmts\> | → | versa ( \<switch-values\> ) { betsung \<switch-values\> : \<loop-switch-statements\> \<loop-multi-cases\> \<ditech-case\> } |
| 189 | \<loop-multi-cases\> | → | betsung \<switch-values\> : \<loop-switch-statements\> \<loop-multi-cases\> |
| 190 | \<loop-multi-cases\> | → | λ |
| 191 | \<loop-switch-statements\> | → | \<local-dec\> \<loop-body\> \<multi-loop-body\> |
| 192 | \<amaccana-case\> | → | amaccana ; |
| 193 | \<amaccana-case\> | → | λ |
| 194 | \<ditech-case\> | → | ditech : \<switch-statements\> |
| 195 | \<ditech-case\> | → | λ |
| 196 | \<control-flow-stmts\> | → | gogogo ; |
| 197 | \<control-flow-stmts\> | → | amaccana ; |
| 198 | \<control-flow-stmts\> | → | λ |
| 199 | \<return-stmts\> | → | push \<push-values\> ;    |
| 200 | \<return-stmts\> | → | λ |
| 201 | \<unary-stmts\> | → | \<unary-operator\> id ; |
| 202 | \<unary-stmts\> | → | id \<unary-operator\> ; |
| 203 | \<push-values\> | → | \<expression\> |
| 204 | \<push-values\> | → | λ |

