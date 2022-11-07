
#include <stdio.h>
#include <pthread.h>


static int data = 0;

void* add(void* args) {

  for(int i = 0; i < 1000; i++) {
    data++;
  }
  return NULL;
}

int main() {
  pthread_t t1, t2;
  pthread_create(&t1, NULL, add, NULL);
  pthread_create(&t2, NULL, add, NULL);
  pthread_join(t1, NULL);
  pthread_join(t2, NULL);
  return 0;
}