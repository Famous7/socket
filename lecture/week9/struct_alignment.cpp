#include <iostream>
using namespace std;

struct MyType1{
  char a;
  double b;
  int c;
};

struct MyType2{
  char a;
  int c;
  double b;
};

int main(int argc, char *argv[]){
  struct MyType1 t1;
  struct MyType2 t2;
  cout << "t1 크기 : " << sizeof(t1) << endl;
  cout << "t2 크기 : " << sizeof(t2) << endl;

  return 0;
}
