// This file was generated by mys. DO NOT EDIT!!!

#pragma once

#include "mys.hpp"

namespace mys::basics
{
class Calc;
#define MYS_BASICS_Calc_IMPORT_AS(__name__) \
    using __name__ = mys::basics::Calc;
class Calc : public Object {
public:
    i32 value;
    void triple();
    Calc(i32 value);
    virtual ~Calc();
    String __str__() const;
};
std::ostream& operator<<(std::ostream& os, const Calc& obj);
std::shared_ptr<Tuple<i32, String>> func_1(i32 a);
#define MYS_BASICS_func_1_IMPORT_AS(__name__) \
    constexpr auto __name__ = [] (auto &&...args) { \
        return mys::basics::func_1(std::forward<decltype(args)>(args)...); \
    };
std::shared_ptr<Dict<i64, std::shared_ptr<List<f64>>>> func_3(i32 a);
#define MYS_BASICS_func_3_IMPORT_AS(__name__) \
    constexpr auto __name__ = [] (auto &&...args) { \
        return mys::basics::func_3(std::forward<decltype(args)>(args)...); \
    };
void func_4(void);
#define MYS_BASICS_func_4_IMPORT_AS(__name__) \
    constexpr auto __name__ = [] (auto &&...args) { \
        return mys::basics::func_4(std::forward<decltype(args)>(args)...); \
    };
std::shared_ptr<List<i64>> func_5(void);
#define MYS_BASICS_func_5_IMPORT_AS(__name__) \
    constexpr auto __name__ = [] (auto &&...args) { \
        return mys::basics::func_5(std::forward<decltype(args)>(args)...); \
    };
}
