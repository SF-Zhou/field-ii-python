#ifndef FUNC_HPP
#define FUNC_HPP

#include <cmath>

#define ff(i, n) for (int i = 0, END = (n); i < END; ++ i)
#define fff(i, n, m) for (int i = (n), END = (m); i <= END; ++ i)

template<class T>
inline T sqr(T a) {
    return a * a;
}

template<class T>
T hypotenuse(T a, T b) {
    return sqrt(sqr(a) + sqr(b));
}

#endif
