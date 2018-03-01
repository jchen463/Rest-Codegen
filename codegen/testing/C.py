import A
import B

B.main()


def run_iterators():
    for iterator_name, iterator in A.iterators_mapping.items():
        iterator(A.iterator_functions_mapping[iterator_name])


run_iterators()
