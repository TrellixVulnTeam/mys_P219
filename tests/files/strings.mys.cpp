#include "mys.hpp"

Tuple<String, String> get();

int main();

Tuple<String, String> get()
{
    /* mys-embedded-c++ start */
    return Tuple<String, String>({"Hello", "!"});
    /* mys-embedded-c++ stop */;
}

int main()
{
    auto value = get();
    auto foo = std::get<0>(*value.m_tuple);
    auto bar = std::get<1>(*value.m_tuple);
    String foo2(foo);
    foo += bar;
    ASSERT(foo == "Hello!");
    ASSERT(foo2 == foo);
    /* mys-embedded-c++ start */
    auto fie = String(foo.m_string->c_str());
    /* mys-embedded-c++ stop */;
    foo += "!";
    ASSERT(foo == "Hello!!");
    ASSERT(fie == "Hello!");

    return 0;
}
