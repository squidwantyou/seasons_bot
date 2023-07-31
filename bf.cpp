#include <iostream>

unsigned char tape[30000] = {0};
unsigned char* ptr = tape;

void interpret(char* input)
{
	unsigned int tmp;
	char current_char;
	unsigned int i, loop;

    for( tmp = 0 ; tmp<15000; tmp ++ ) {
        ++ptr;
    }
	
	for (i = 0; input[i] != 0; ++i)
	{
		current_char = input[i];

		switch (current_char)
		{
			case '>':
				++ptr;
				break;
			case '<':
				--ptr;
				break;
			case '+':
				++*ptr;
				break;
			case '-':
				--*ptr;
				break;
			case '.':
				putchar(*ptr);
				break;
			case ',':
				*ptr = getchar();
				break;
			case '[':
				if (*ptr == 0)
				{
					loop = 1;
					while (loop > 0)
					{
						current_char = input[++i];
						if (current_char == '[')
							loop++;
						else if (current_char == ']')
							loop--;
					}
				}
				break;
			case ']':
				if (*ptr)
				{
					loop = 1;
					while (loop > 0)
					{
						current_char = input[--i];
						if (current_char == '[')
							loop--;
						else if (current_char == ']')
							loop++;
					}
				}
		}
	}
}

int main()
{

	char str[1024];
	std::cin.get(str, 1024);
	
	interpret(str);
	putchar('\n');

	return 0;
}
