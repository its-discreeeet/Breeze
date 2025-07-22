#include<stdio.h>
#include<string.h>

int a;
struct student{
		int roll_no;
		char name[20];
		float marks;
};

void accept(struct student s1[a],int n){
	
	for(int i=0;i<n;i++){
		printf("Enter roll no:");
		scanf("%d",&s1[i].roll_no);
		printf("Enter name:");
		scanf("%s",s1[i].name);
		printf("Enter marks:");
		scanf("%f",&s1[i].marks);
	}
}
void display(struct student s1[a],int m){
	printf("\t*************************************\n");
	printf("\tRoll_no\t\tName\t\tMarks\n");
	for(int i=0;i<m;i++){
		printf("\t%d\t",s1[i].roll_no);
		printf("\t%s\t",s1[i].name);
		printf("\t%f\t\n",s1[i].marks);
	}
}
int linear_search(struct student s1[a],int c,int o){
	int i;
	for(i=0;i<a;i++){
		
		if(s1[i].roll_no==c){
			printf("Target Found\n");
			break;
		}
	}
	if(i==o){
		printf("Target Not Found\n");
		return -1;
	}
	return i;
}
void selection_sort(struct student s1[a],int n){
	int minpos,i,j;
	struct student temp;
	int pass=0;
	for(i=0;i<=n-2;i++){
		pass++;
		minpos=i;
		for(j=i+1;j<=n-1;j++){
			if(s1[j].roll_no<s1[minpos].roll_no){
				minpos=j;
			}
		}
		if(minpos!=i){
			temp=s1[i];
			s1[i]=s1[minpos];
			s1[minpos]=temp;
		}
		
	}
	display(s1,a);
	printf("No. of passes = %d",pass);
}
void insertion_sort(struct student s1[a],int n){
	
	int i,j;
	struct student key;
	for(i=1;i<n;i++){
		key=s1[i];
		j=i-1;
		while(j>=0 && s1[j].roll_no>key.roll_no){
			s1[j+1]=s1[j];
			j=j-1;
		}
		s1[j+1]=key;
	}
	display(s1,a);
}

void shell_sort(struct student s[a],int n){
	int gap,swap,i;
	struct student temp;
	gap=n/2;
	
	do{
		do{
	            swap=0;
		    for(i=0;i<n-gap;i++){
			if(s[i].roll_no>s[i+gap].roll_no){
				temp=s[i];
				s[i]=s[i+gap];
				s[i+gap]=temp;
				swap=1;
			}
		}
	}while(swap==1);
}while( (gap /=2)>=1);

display(s,a);
}

int bsr(struct student s1[10],int low, int high, int key){
     int mid;
     if(low<=high) {
     mid=(low+high)/2;

	if(s1[mid].roll_no == key){
		printf("\n%d %s %f", s1[mid].roll_no,s1[mid].name,s1[mid].marks);
		return mid; 
		}

		else if(key < s1[mid].roll_no) {
			return bsr(s1,low,mid-1,key);
		}

		else {
			return bsr(s1,mid+1,high,key);
		}
	return -1;
     }
		
	
}
int main(){
	int low=0;
	printf("Enter no of elements to be inserted:\n");
	scanf("%d",&a);
	int high = a-1;
	int ch;
	struct student s1[a];
	
	accept(s1,a);
	display(s1,a);

//	linear_search(s1,b,a);
//	selection_sort(s1,a);
//	insertion_sort(s1,a);
	printf("Enter choice which you want to perform:\n");
	printf("1.Sorting\n2.Searching :- ");
	scanf("%d",&ch);
	switch(ch){
		case 1:
			int ch3;
			printf("Enter your choice:\n1.insertion sort\n2.selection sort\n3.Shell Sort :- ");
			scanf("%d",&ch3);
			switch(ch3){
				case 1:
					insertion_sort(s1,a);
					break;
				
				case 2:
					selection_sort(s1,a);
					break;
				case 3:
					shell_sort(s1,a);
					break;
	
				default:
					printf("Enter valid choice");
				
			}
			break;



		case 2:
			int ch2;
			int b;
			printf("Enter roll no to be searched:");
			scanf("%d",&b);
			printf("Enter your choice:\n1.Linear search\n2.Binary search\n");
			scanf("%d",&ch2);
			switch(ch2){
				case 1:
					linear_search(s1,b,a);
					break;
				
				case 2:
					selection_sort(s1,a);
					bsr(s1,low,high,b);
					break;
				
				default:
					printf("Enter valid choice");
			}
			break;
		
	}
	return 0;
}



