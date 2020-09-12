// This file was generated by mys. DO NOT EDIT!!!

#include "message_passing/main.mys.hpp"

namespace message_passing::main
{

int main(int __argc, const char *__argv[]);

int main(int __argc, const char *__argv[])
{
    (void)__argc;
    (void)__argv;
    auto calculator = std::make_shared<message_passing::calculator::Calculator>();
    auto student = std::make_shared<message_passing::student::Student>();
    calculator->student = student;
    student->calculator = calculator;
    calculator->start();
    student->start();
    std::cout << "Press any key to exit.";
    char c;
    std::cin >> c;
    mys::thread::Thread::send_stop(std::make_shared<mys::thread::Stop>("Bye!"));
    mys::thread::Thread::join();
    std::cout << "Done!" << std::endl;

    return 0;
}

}

int package_main(int argc, const char *argv[])
{
    return message_passing::main::main(argc, argv);
}
