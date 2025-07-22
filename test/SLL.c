#include<stdio.h>
#include<stdlib.h>
#include<string.h>

struct student 
{
    int prn;
    char name[20];
    char pos[20];
    char year[20];
    struct student*next;
};

void create(struct student*h);
void display(struct student*h);
void insert(struct student*h);
void delete(struct student*h);
void reverse(struct student*h);
void sort(struct student*h);
void merge(struct student*h1,struct student*h2);
void length(struct student*h);
int length2(struct student*h);

int main()
{
    struct student*head=(struct student*)malloc(sizeof(struct student));
    head->next=NULL;
    struct student*head2=(struct student*)malloc(sizeof(struct student));
    head2->next=NULL;
    printf("\n*********PINNACLE CLUB**********\n");
    printf("It is a student club for the department of computer science and engineering\n");

    int a;
    int flag = 1;
    while(flag==1)
    {
        printf("Which operation do want to perform?\n");
        printf("1.Creation of list\n");
        printf("2.Display of list\n");
        printf("3.Inserting new member in the list\n");
        printf("4.Deleting a member from the list\n");
        printf("5.Number of members in the list\n");
        printf("6.Sorting the list based on thier prn\n");
        printf("7.Reversing the order of the list\n");
        printf("8.Merge another list in your previous list\n");
        printf("9.Exit all operations\n");
        
        scanf("%d",&a);
        
        switch(a)
        {
            case 1:
            create(head);
            break;

            case 2:
            display(head);
            break;

            case 3:
            insert(head);
            break;

            case 4:
            delete(head);
            break;

            case 5:
            length(head);
            break;

            case 6:
            sort(head);
            break;

            case 7:
            reverse(head);
            break;

            case 8:
            printf("Create a linked list to be merged\n");
            create(head2);
            display(head2);
            sort(head2);
            printf("merged list is : \n");
            merge(head,head2);

            case 9:
            flag=0;
            // break;

        }
    }
    
    return 0;
}

void length(struct student*h)
{
    int i=0;
    if(h->next==NULL)
    {
        i=0;
    }
    else
    {
        struct student*temp=h->next;
        while(temp!=NULL)
        {
            temp=temp->next;
            i++;
        }
    }
    printf("No. of members including the president and the secretary is %d\n",i);
}

int length2(struct student*h)
{
    int i=0;
    if(h->next==NULL)
    {
        i=0;
    }
    else
    {
        struct student*temp=h->next;
        while(temp!=NULL)
        {
            temp=temp->next;
            i++;
        }
    }
    return i;
}

void create(struct student* h) 
{
    struct student* temp = h;
    char ch;
    printf("Here are some rules for the representation and creation of the list\n");
    printf("First-year students are not eligible for this club\n");
    printf("The year of the students can be represented as: \n");
    printf("second - 'sd'\n");
    printf("third - 'td'\n");
    printf("fourth - 'ft'\n");
    printf("The position of the students can be represented as: \n");
    printf("president - 'ps'\n");
    printf("secretary - 'st'\n");
    printf("member - 'mb'\n");

    printf("\nEnter Details for president : \n");
    struct student* curr = (struct student*)malloc(sizeof(struct student));
    curr->next = NULL;
    temp->next = curr;
    temp = curr;

    printf("Enter name : ");
    scanf("%s", curr->name);
    printf("Enter prn : ");
    scanf("%d", &curr->prn);
    strcpy(curr->pos, "ps");
    printf("Enter year : ");
    scanf("%s", curr->year);

    printf("\nEnter Details for secretary : \n");
    curr = (struct student*)malloc(sizeof(struct student));
    curr->next = NULL;
    temp->next = curr;
    temp = curr;

    printf("Enter name : ");
    scanf("%s", curr->name);
    printf("Enter prn : ");
    scanf("%d", &curr->prn);
    strcpy(curr->pos, "st");
    printf("Enter year : ");
    scanf("%s", curr->year);

    printf("\nEnter Details for the members of the club: \n");
    int i = 3;
    do {
        printf("\nstudent %d\n", i);
        curr = (struct student*)malloc(sizeof(struct student));
        curr->next = NULL;
        temp->next = curr;
        temp = curr;

        printf("Enter name : ");
        scanf("%s", curr->name);
        printf("Enter prn : ");
        scanf("%d", &curr->prn);
        strcpy(curr->pos, "mb");
        printf("Enter year : ");
        scanf("%s", curr->year);

        i++;
        printf("\nDo you want to add more members?\n");
        printf("Enter 'y' for yes else press any key: ");
        scanf(" %c", &ch);
    } while (ch == 'y' || ch == 'Y');
}

void display(struct student*h)
{

    if(h->next==NULL)
    {
        printf("\nlist is empty");
    }
    else
    {
        printf("\nDisplaying the records of the club\n");
        printf("PRN\tName\tPosition\tYear\n");
        struct student*temp=h->next;
        while(temp!=NULL)
        {
            printf("%d\t%s\t%s\t\t%s\n",temp->prn,temp->name,temp->pos,temp->year);
            temp=temp->next;
        }
    }
}


void insert(struct student*h)
{
    int i=1;
    struct student*curr=h;
    int pos2;
    printf("Positions of president and secretary can not be changed\n");
    printf("So position to be entered must be greater than 2\n");
    printf("Enter the position at which you want to insert data: ");
    scanf("%d",&pos2);
    int l=length2(h);
    if(pos2 > l && pos2 < 2)
    {
        printf("Data can not be inserted.\n");
    }
    else
    {
        struct student *nnode = (struct student*)malloc(sizeof(struct student));
        printf("Enter name : ");
        scanf("%s",nnode->name);
        printf("Enter prn : ");
        scanf("%d",&nnode->prn);
        printf("Enter position : ");
        scanf("%s",nnode->pos);
        printf("Enter year : ");
        scanf("%s",nnode->year);
    
        while(curr!=NULL&&i<pos2)  //important
        {
			i++;
			curr=curr->next;
		}
		nnode->next=curr->next;
		curr->next=nnode;
    }
}

void delete(struct student*h)
{
    
	int pos2;
	struct student *prev=h;
	int ctr=1;
	struct student *curr=h;
	curr=h->next;
	printf("Enter the position at which you want to delete: ");
	scanf("%d",&pos2);
	int l=length2(h);

	if(l<pos2)
    {
		printf("Invalid position");
	}
	else
    {
		while(ctr<pos2 && curr!=NULL)
        {
			ctr++;
			prev=curr;
			curr=curr->next;
		}
		struct student *temp=curr;
		prev->next=curr->next;
		curr->next=NULL;
		free(temp);

	}
}

void reverse(struct student*h)
{
    struct student*prev=NULL;
    struct student*curr=h->next;
    while(curr!=NULL)
    {
        // int a=strcmp(curr->pos,"ps");
        // int b=strcmp(curr->pos,"st");
        // if(a==0 || b==0)
        // {
        //     continue;
        // }
        // else
        // {
            struct student*future = curr->next;
            curr -> next = prev;
            prev = curr;
            curr = future;
        // }
    }
    h->next=prev;
}

void sort(struct student*h)
{
    int l=length2(h);

    for(int i=0; i<l-1; i++)
    {
        struct student*prev=h;
        struct student*curr=h->next;
        for(int j=0; j<l-1; j++)
        {
            // int a=strcmp(curr->pos,"ps");
            // int b=strcmp(curr->pos,"st");
            // if(a==0 || b==0)
            // {
            //     continue;
            // }
            // else
            // {
                struct student*temp=curr->next;
                if(curr->prn > temp->prn)
                {
                    prev->next=temp;
                    curr->next=temp->next;
                    temp->next=curr;
                    prev=temp;
                }
                else
                {
                    prev=curr;
                    curr=curr->next;
                }
            // }
        }
    }
}

void merge(struct student*h1, struct student*h2)
{
    struct student*curr1=h1->next;
    struct student*curr2=h2->next;
    int flag;
    struct student*temp;
    if(curr1->prn < curr2->prn)
    {
        temp=h1;
        flag=1;
    }
    else
    {
        temp=h2;
        flag=0;
    }
    while(curr1!=NULL && curr2!=NULL)
    {
        if(curr1->prn < curr2->prn)
        {
            temp->next=curr1;
            temp=curr1;
            curr1=curr1->next;
        }
        else
        {
            temp->next=curr2;
            temp=curr2;
            curr2=curr2->next;
        }
    }
    if(curr1==NULL)
        temp->next=curr2;
    
    if(curr2==NULL)
        temp->next=curr1;

    if(flag==1)
        display(h1);
    else
        display(h2);
}
