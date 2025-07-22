#include<stdio.h>

struct student{   // student structure.
char name[30];
int roll;
int marks;
};

void accept(struct student s[], int n){
printf("\nEnter following details------->\n");
for(int i = 0; i<n; i++){
    printf("name = ");
    scanf("%s", s[i].name);
    printf("rollno = ");
    scanf("%d", &s[i].roll);
    printf("marks = ");
    scanf("%d", &s[i].marks);
    printf("\n");
}
}

void display(struct student s[], int n){
printf("\n<--------STUDENT DATABASE-------->");
printf("\n"); 
 printf("\n\tName\tRollNo\t Marks\n");
for(int i = 0; i<n; i++){

 printf("\n\t%s \t %d \t %d\n",s[i].name, s[i].roll, s[i].marks);
}
printf("\n<-------------------------------->\n");
}

int getmax(struct student s[], int n){
int max = s[0].marks; 

    for (int i = 1; i < n; i++)  
    if (s[i].marks > max)  
      max = s[i].marks;    
  return max;
}

void bucket(struct student s[], int n) // function to implement bucket sort  
{  
  int max = getmax(s, n); //max is the maximum element of array  
  int bucket[max], i;  
  for (int i = 0; i <= max; i++)  
  {  
    bucket[i] = 0;  
  }  
  for (int i = 0; i < n; i++)  
  {  
    bucket[s[i].marks]++;  
  }  
  for (int i = 0, j = 0; i <= max; i++)  
  {  
    while (bucket[i] > 0)  
    {  
      s[j++].marks = i;  
      bucket[i]--;  
    }  
  }  
}

void countingSort(struct student s[], int n, int place) // function to implement counting sort  
{  
  int output[n + 1];  
  int count[10] = {0};    
  
  // Calculate count of elements  
  for (int i = 0; i < n; i++)  
    count[(s[i].marks / place) % 10]++;  
      
  // Calculate cumulative frequency  
  for (int i = 1; i < 10; i++)  
    count[i] += count[i - 1];  
  
  // Place the elements in sorted order  
  for (int i = n - 1; i >= 0; i--) {  
    output[count[(s[i].marks / place) % 10] - 1] = s[i].marks;  
    count[(s[i].marks / place) % 10]--;  
  }  
  
  for (int i = 0; i < n; i++)  
    s[i].marks = output[i];  
}


// function to implement radix sort  
void radix(struct student s[], int n) {  
   
  // get maximum element from array  
  int max = getmax(s, n);  
  
  // Apply counting sort to sort elements based on place value  
  for (int place = 1; max / place > 0; place *= 10)  
    countingSort(s, n, place);  
}





int main(){

int choice;
int n;
printf("\n ENTER NUMBER OF STUDENTS = ");
scanf("%d",&n);
printf("\n");

struct student s[n];
accept(s, n);
display(s, n);

printf("\n");

printf("*******SELECT SORTING METHOD*******\n");
printf("1. BUCKET SORT \n");
printf("2. RADIX SORT \n");
printf("***********************************\n\n");
printf("enter choice = ");
scanf("%d",&choice);

switch (choice)
{
case 1:
  printf("SORTED USING BUCKET SORT...\n");
  bucket(s, n);
  display(s ,n);
  break;

case 2:
  printf("SORTED USING RADIX SORT...\n");
  radix(s, n);
  display(s ,n);
  break;

default:
  break;
}

  return 0; 
 }