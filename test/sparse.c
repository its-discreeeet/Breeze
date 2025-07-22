#include<stdio.h>

int sparse_row(int a[10][10],int m, int n)
{
    int k=1;
    for(int i=0; i<m; i++)
    {
        for(int j=0; j<n; j++)
        {
            if(a[i][j]!=0)
            {
                k++;
            }
        }
    }
    return k;
}

void compact(int a[10][10],int m, int n, int b[20][3])
{
    printf("\nthe sparse matrix is as follows :\n");
    b[0][0]=m;
    b[0][1]=n;
    int k=1;
    for(int i=0; i<m; i++)
    {
        for(int j=0; j<n; j++)
        {
            if(a[i][j]!=0)
            {
                b[k][0]=i;
                b[k][1]=j;
                b[k][2]=a[i][j];
                k++;
            }
        }
    }
    b[0][2]=k-1;
    for (int i = 0; i <= k-1; i++)
    {
        printf("%d\t%d\t%d\n", b[i][0], b[i][1], b[i][2]);
    }
}

void transpose(int b[20][3],int c[20][3])
{
    int m=b[0][0];
    int n=b[0][1];
    int t=b[0][2];
    int q=1;
    c[0][0]=n;
    c[0][1]=m;
    c[0][2]=t;
    printf("The transpose of matrix in compact form is :\n");
    if (t<=0)
    {
        return -1;
    }
    for(int x=0; x<n ;x++)
    {
        for(int p=1;p<=t;p++)
        {
            if(b[p][1]==x)
            {
                c[q][0]=b[p][1];
                c[q][1]=b[p][0];
                c[q][2]=b[p][2];
                q=q+1;
            }
        }
    }
    c[0][2]=t;

    for (int i = 0; i <= t; i++)
    {
        printf("%d\t%d\t%d\n", c[i][0], c[i][1], c[i][2]);
    }
}

void fast_trans(int b[20][3],int c[20][3])
{
    int m=b[0][0];
    int n=b[0][1];
    int t=b[0][2];

    c[0][0]=n;
    c[0][1]=m;
    c[0][2]=t;
    int S[n],T[n];  // local array
    printf("The fast transpose of matrix in compact form is :\n");
    if (t<=0)
    {
        return -1;
    }
    for(int i=0; i<n; i++)
    {
        S[i]=0;
    }
    
    for(int i=0; i<=t; i++)
    {
        S[b[i][1]]++;
    }

    T[0]=1;
    for(int i=1; i<n; i++)
    {
        T[i]= T[i -1] + S[i - 1];
    }

    for (int i=1; i<=t; i++)
    {
        int j = b[i][1];
        c[T[j]][0]=b[i][1];
        c[T[j]][1]=b[i][0];
        c[T[j]][2]=b[i][2];
        T[j]=T[j]+1;
    }
    c[0][2]=t;

    for (int i = 0; i <= t; i++)
    {
        printf("%d\t%d\t%d\n", c[i][0], c[i][1], c[i][2]);
    }
}

int main()
{
    // int max;
    int a[10][10],i,j,m,n;
    // int max=sparse_row(a,m,n);
    int b[20][3];
    int c[20][3];
    int d[20][3];
    
    printf("Enter no. of rows : ");
    scanf("%d", &m);
    printf("\nEnter no. of cols : ");
    scanf("%d",&n);
    printf("\nEnter values to the matrix \n");
    for (i = 0; i < m; i++)
    {
        for (j = 0; j < n; j++)
        {
            printf("\nEnter a[%d][%d] value : ",i,j);
            scanf("%d", &a[i][j]);
        }
    }
    
    printf("\nThe given matrix is \n");
    for (i = 0; i < m; ++i)
    {
        for (j = 0; j < n; ++j)
        {
            printf("%d\t", a[i][j]);
        }
        printf("\n");
    }
    
    compact(a,m,n,b);
    
    int y=0;
    do{
        printf("Which type of transpose do want to perform?\n1.Simple Transpose\n2.Fast Transpose?\n");
        int x;
        scanf("%d",&x);
        switch(x)
        {
            case 1:
            transpose(b,c);
            y++;
            break;
            
            case 2:
            fast_trans(b,d);
            y++;
            break;
            
            default:
            printf("enter valid input\n");
        }
    }while(y<2);
    
    return 0;
}
