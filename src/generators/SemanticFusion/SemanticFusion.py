import random
import copy

from src.parsing.parse import *
from src.generators.Generator import Generator
from src.generators.SemanticFusion.MetamorphicTuple import *
from src.generators.SemanticFusion.util import *

class SemanticFusion(Generator):
    def __init__(self, seeds, oracle, config_file):
        super().__init__(seeds,config_file)
        assert(len(seeds) == 2)
        self.formula1, self.formula2 = parse_file(seeds[0],silent=False), parse_file(seeds[1], silent=False)

        self.config_file = config_file
        self.oracle = oracle
        self.templates = {}
        self._parse_mrs()

        if not self.oracle:
            print("ERROR: No oracle {sat,unsat} specified")
            exit(1)

    def _parse_mrs(self):
        with open(self.config_file) as f:
            lines = f.readlines()
        started=False
        curr = []
        _mrs = []

        for l in lines:
            if ";" in l: continue
            if not l.strip(): continue
            if "begin" in l:
                started = True
                continue
            if "end" in l:
                started = False
                _mrs.append("\n".join(curr))
                curr = []
                continue
            if started:
                curr.append(l)

        print('_mrs:', _mrs)
        for i,mr in enumerate(_mrs):
            template = parse_str(mr)
            sort = template.commands[0].sort

            if not sort in self.templates:
                self.templates[sort] = [template]
            else:
                self.templates[sort].append(template)
        print('parser_mrs::template:', self.templates)


    def fuse(self, occs1, occs2, formula1, formula2, metamorphic_tuples):
        print('fusing....')
        print('occs1:---------------\n', occs1, sep='')
        print('occs2:---------------\n', occs2, sep='')
        fusion_constr = []
        vars = []
        print('metamorphic_tuples:', metamorphic_tuples.__str__())
        for t in metamorphic_tuples:
            print(' [before] t:', t.__str__())
            t.x.substitute(t.x, t.x_substituent())
            t.y.substitute(t.y, t.y_substituent())
            print(' [after] t:', t.__str__())
            fusion_constr += t.xyz_constraints()
            print('vars:', vars)
            if not t.z in vars:
                vars.append(t.z)
                print('vars+t.z:', vars)
            print()
            print('fusion_constr:')
            for m in fusion_constr:
                print(m.__str__())
        if self.oracle == "sat":
            formula = conjunction(formula1, formula2)
            print('conjunct the formulas:')
            print(formula)
        else:
            formula = disjunction(formula1, formula2)
            add_fusion_constraints(formula, fusion_constr)
        add_var_decls(formula, vars)
        print()
        print('add vars:')
        print(formula)
        return formula


    def generate(self):
        print('call semanticfusion::generate')
        if self.formula1.free_var_occs == [] or self.formula2.free_var_occs == []:
            return None, False
        formula1, formula2 = copy.deepcopy(self.formula1), copy.deepcopy(self.formula2)
        print('before prefix....')
        print('formula1:---------------\n', formula1, sep='')
        print('formula2:---------------\n', formula2, sep='')
        print('\nafter prefix....')
        formula1.prefix_vars("scr1_")
        formula2.prefix_vars("scr2_")
        print('formula1:---------------\n', formula1, sep='')
        print('formula2:---------------\n', formula2, sep='')
        occs1, occs2 = formula1.free_var_occs, formula2.free_var_occs
        print('\nget occs:')
        print('occs1:---------------\n', occs1, sep='')
        print('occs2:---------------\n', occs2, sep='')
        print('\ndo random mr tuples')
        metamorphic_tuples = random_mr_tuples(occs1, occs2, self.templates)
        if not metamorphic_tuples:
            return None, False
        fused = self.fuse(occs1, occs2, formula1, formula2, metamorphic_tuples)
        return fused, True
