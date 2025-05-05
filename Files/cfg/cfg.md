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
| 17 | \<func-array-init-tail\> | → | \<array-dec\> \<array-init\> |
| 18 | \<func-case\> | → | ( \<parameters\> ) |
| 19 | \<parameters\> | → | \<func-parameters\> \<multi-parameters\> |
| 20 | \<parameters\> | → | λ  |
| 21 | \<func-parameters\> | → | \<data-type\> id \<array-dec\> |
| 22 | \<multi-parameters\> | → | , \<func-parameters\> \<multi-parameters\> |
| 23 | \<multi-parameters\> | → | λ |
| 24 | \<array-dec\> | → | \[ \] |
| 25 | \<array-dec\> | → | λ |
|  | \<array-indexing\> | → | \[ \<array-values\> \] \<2d-index\>  |
|  | \<array-indexing\> | → | λ |
| 26 | \<2d-index\> | → | \[ \<array-values\> \] \<3d-index\> |
| 27 | \<2d-index\> | → | λ |
| 28 | \<3d-index\>  | → | \[ \<array-values\> \] |
| 29 | \<3d-index\>  | → | λ |
| 30 | \<array-values\> | → | \<expression\> |
| 31 | \<literals\> | → | anda\_literal |
| 32 | \<literals\> | → | andamhie\_literal |
| 33 | \<literals\> | → | chika\_literal \<array-indexing\> |
| 34 | \<literals\> | → | \<eklabool\> |
| 35 | \<eklabool\> | → | korik |
| 36 | \<eklabool\> | → | eme |
| 37 | \<func-array\>  | → | \<func-array-value\> |
| 38 | \<func-array\>   | → | λ |
| 39 | \<func-array-value\> | → | ( \<arguments\> ) |
| 40 | \<func-array-value\> | → | \<array-indexing\> |
| 41 | \<var-init\>  | → | id \<var-init-tail\> \<multi-init-values\> |
| 42 | \<var-init-tail\>  | → | \= \<init-values\> |
| 43 | \<var-init-tail\>  | → | λ |
| 44 | \<multi-init-values\> | → | , id \<multi-init-values-tail\> \<multi-init-values\> |
| 45 | \<multi-init-values\> | → | λ |
| 46 | \<multi-init-values-tail\> | → | \= \<init-values\>  |
| 47 | \<multi-init-values-tail\> | → | λ |
| 48 | \<init-values\> | → | \<expression\> |
| 49 | \<array-init\> | → | \= { \<array-elements\> } |
|  | \<array-init\> | → | \= id |
| 50 | \<array-init\> | → | λ |
| 51 | \<array-elements\> | → | \<array-values\> \<extra-array-value\> |
|  | \<array-elements\> | → | { \<array-elements\> } \<extra-array-value\> |
| 56 | \<extra-array-value\> | → | , \<array-values\> \<extra-array-value\> |
|  | \<extra-array-value\> | → | , { \<array-elements\> } \<extra-array-value\> |
| 57 | \<extra-array-value\> | → | λ |
| 63 | \<func-def\> | → | \<return-type\> id ( \<parameters\> ) { \<func-body\> } \<func-def\> |
| 64 | \<func-def\> | → | λ |
| 65 | \<func-body\> | → | \<statements\>  |
| 66 | \<func-body\> | → | λ |
| 67 | \<local-dec\> | → | \<local-dec-init\> \<array-assign\> \<local-dec\> |
| 68 | \<local-dec\> | → | λ |
| 69 | \<local-dec-init\> | → | \<naur-case\> \<data-type\> \<var-init\> ;  |
| 70 | \<local-dec-init\> | → | \<data-type\> id \<array-dec\> \<array-init\> ;  |
| 71 | \<arguments\> | → | \<arguments-value\> \<multi-arguments-value\> |
| 72 | \<arguments\> | → | λ |
| 73 | \<multi-arguments-value\> | → | , \<arguments-value\> \<multi-arguments-value\> |
| 74 | \<multi-arguments-value\> | → | λ |
| 75 | \<arguments-value\> | → | \<expression\> |
| 76 | \<array-assign\> | → | id \<array-indexing\> \= \<array-values\> ; |
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
|  | \<expression-value\> | → | len ( \<len-choice\> ) |
|  | \<len-choice\> | → | chika\_literal |
|  | \<len-choice\> | → | id \<array-indexing\> |
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
| 114 | \<statements\> | → | id \<assign-call-stmts\> \<statements\> |
| 115 | \<statements\> | → | \<input-stmts\> \<statements\> |
| 116 | \<statements\> | → | \<output-stmts\> \<statements\> |
|  | \<statements\> | → | \<append-stmts\> \<statements\> |
|  | \<statements\> | → | \<delete-stmts\> \<statements\> |
| 117 | \<statements\> | → | \<conditional-stmts\> \<statements\> |
| 118 | \<statements\> | → | \<loop-stmts\> \<statements\> |
| 119 | \<statements\> | → | \<switch-stmts\> \<statements\> |
| 120 | \<statements\> | → | \<return-stmts\> \<statements\> |
| 121 | \<statements\> | → | \<unary-stmts\> \<statements\> |
|  | \<statements\> | → | \<local-dec\> \<statements\> |
| 122 | \<statements\> | → | λ |
| 123 | \<loop-body\> | → | id \<assign-call-stmts\> \<statements\> |
| 124 | \<loop-body\> | → | \<input-stmts\> \<loop-body\> |
| 125 | \<loop-body\> | → | \<output-stmts\> \<loop-body\> |
|  | \<loop-body\> | → | \<append-stmts\> \<loop-body\> |
|  | \<loop-body\> | → | \<delete-stmts\> \<loop-body\> |
| 126 | \<loop-body\> | → | \<loop-stmts\> \<loop-body\> |
| 127 | \<loop-body\> | → | \<loop-conditional-stmts\> \<loop-body\> |
| 128 | \<loop-body\> | → | \<loop-switch-stmts\> \<loop-body\> |
| 129 | \<loop-body\> | → | \<return-stmts\> \<loop-body\> |
| 130 | \<loop-body\> | → | \<unary-stmts\> \<loop-body\> |
| 131 | \<loop-body\> | → | \<control-flow-stmts\> \<loop-body\> |
|  | \<loop-body\> | → | \<local-dec\> \<loop-body\> |
| 132 | \<loop-body\> | → | λ |
| 133 | \<multi-loop-body\> | → | \<loop-body\> \<multi-loop-body\> |
| 134 | \<multi-loop-body\> | → | λ |
| 135 | \<assign-call-stmts\> | → | \<array-indexing\> \<assignment-operators\> \<assignment-values\> ; |
| 136 | \<assign-call-stmts\> | → | ( \<arguments\> ) ; |
| 137 | \<assignment-operators\> | → | \= |
| 138 | \<assignment-operators\> | → | \+= |
| 139 | \<assignment-operators\> | → | \-= |
| 140 | \<assignment-operators\> | → | %= |
| 141 | \<assignment-operators\> | → | /= |
| 142 | \<assignment-operators\> | → | //= |
| 143 | \<assignment-operators\> | → | \*= |
| 144 | \<assignment-operators\> | → | \*\*= |
| 145 | \<assignment-values\> | → | \<expression\> |
|  | \<assignment-values\> | → | { \<array-elements\> } |
| 146 | \<input-stmts\> | → | \<input-type\> id \= givenchy ( \<givenchy-values\> ) ; |
| 147 | \<input-type\> | → | \<data-type\> |
| 148 | \<input-type\> | → | λ |
| 149 | \<givenchy-values\> | → | \<expression-operands\> |
| 150 | \<output-stmts\> | → | serve ( \<output-values\> ) ; |
|  | \<append-stmts\> | → | adele ( id \<array-indexing\> , \<assignment-values\> ) ; |
|  | \<delete-stmts\> | → | adelete ( id \<array-indexing\> ) ; |
| 151 | \<output-values\> | → | \<expression\> |
| 152 | \<conditional-stmts\> | → | pak ( \<condition\> ) { \<conditional-body\> } \<ganern-pak-statement\> \<ganern-case\> |
| 153 | \<condition\> | → | \<expression\> |
| 154 | \<conditional-body\> | → | \<statements\>  |
| 155 | \<conditional-body\> | → | λ |
| 156 | \<loop-conditional-stmts\> | → | pak ( \<condition\> ) { \<loop-conditional-body\> } \<ganern-pak-statement\> \<ganern-case\> |
| 157 | \<loop-conditional-body\> | → | \<loop-body\> \<multi-loop-body\> |
| 158 | \<loop-conditional-body\> | → | λ |
| 159 | \<ganern-pak-statement\> | → | ganern pak ( \<condition\> ) { \<conditional-body\> } \<ganern-pak-statement\> |
| 160 | \<ganern-pak-statement\> | → | λ |
| 161 | \<ganern-case\> | → | ganern { \<conditional-body\> } |
| 162 | \<ganern-case\> | → | λ |
| 163 | \<loop-stmts\> | → | \<forda-statement\> |
| 164 | \<loop-stmts\> | → | \<keri-statement\> |
| 165 | \<forda-statement\> | → | forda ( \<loop-type-init\> id from \<start-value\> to \<end-value\> \<step-case\> ) { \<for-loop-body\> } |
| 166 | \<loop-type-init\> | → | \<data-type\> |
| 167 | \<loop-type-init\> | → | λ |
| 168 | \<start-value\> | → | \<loop-conditions\> |
| 169 | \<end-value\> | → | \<loop-conditions\> |
| 170 | \<step-case\> | → | step \<update\> |
| 171 | \<step-case\> | → | λ |
| 172 | \<update\> | → | \<expression\> |
| 173 | \<update\> | → | λ |
| 174 | \<loop-conditions\> | → | \<expression\> |
| 175 | \<for-loop-body\> | → | \<loop-body\> \<multi-loop-body\> |
| 176 | \<for-loop-body\> | → | λ |
| 177 | \<keri-statement\> | → | keri \<keri-case\>  |
| 178 | \<keri-case\> | → | ( \<condition\> ) { \<while-loop-body\> } |
| 179 | \<keri-case\> | → | lang { \<while-loop-body\> } keri ( \<condition\> ) |
| 180 | \<while-loop-body\> | → | \<loop-body\> \<multi-loop-body\> |
| 181 | \<while-loop-body\> | → | λ |
| 182 | \<switch-stmts\> | → | versa ( \<switch-values\> ) { betsung \<switch-values\> : \<switch-statements\> \<amaccana-case\> \<multi-cases\> \<ditech-case\> } |
| 183 | \<multi-cases\> | → | betsung \<switch-values\> : \<switch-statements\> \<amaccana-case\> \<multi-cases\> |
| 184 | \<multi-cases\> | → | λ |
| 185 | \<switch-values\> | → | \<expression\> |
| 186 | \<switch-statements\> | → | \<statements\>  |
| 187 | \<loop-switch-stmts\> | → | versa ( \<switch-values\> ) { betsung \<switch-values\> : \<loop-switch-statements\> \<loop-multi-cases\> \<ditech-case\> } |
| 188 | \<loop-multi-cases\> | → | betsung \<switch-values\> : \<loop-switch-statements\> \<loop-multi-cases\> |
| 189 | \<loop-multi-cases\> | → | λ |
| 190 | \<loop-switch-statements\> | → | \<loop-body\> \<multi-loop-body\> |
| 191 | \<amaccana-case\> | → | amaccana ; |
| 192 | \<amaccana-case\> | → | λ |
| 193 | \<ditech-case\> | → | ditech : \<switch-statements\> |
| 194 | \<ditech-case\> | → | λ |
| 195 | \<control-flow-stmts\> | → | gogogo ; |
| 196 | \<control-flow-stmts\> | → | amaccana ; |
| 197 | \<control-flow-stmts\> | → | λ |
| 198 | \<return-stmts\> | → | push \<push-values\> ;    |
| 199 | \<return-stmts\> | → | λ |
| 200 | \<unary-stmts\> | → | \<unary-operator\> id ; |
| 201 | \<unary-stmts\> | → | id \<unary-operator\> ; |
| 202 | \<push-values\> | → | \<expression\> |
|  | \<push-values\> | → | { \<array-elements\> } |
| 203 | \<push-values\> | → | λ |

