| Lettre | Explication | 
|-----------|-----------|
| T | Raspberry Pi connection & identification | 
| H | led ON | 
| L | led OFF | 
| A | run inline asm: reverse engineering part | 
| Z | readback registers r16 to r25 content, Arduino ---serial---> control PC | 
| P | enter user PIN | 
| 3 | set g_ptc = 3 | 
| R | read user PIN | 
| V | call verify PIN | 
| W | call verify PIN asm | 
| X | call verify PIN hardened | 
| S | print status (i.e. g_ptc and g_authenticated) | 
| C | close session, ie set g_authenticated to BOOL_FALSE | 
| N | call new PIN function, ie enter a new cardPIN if g_authenticated = BOOL_TRUE | 
| E | encryption, AES-128 | 
| K | enter AES-128 key and derive round keys (require g_authenticated = BOOL_TRUE) | 
