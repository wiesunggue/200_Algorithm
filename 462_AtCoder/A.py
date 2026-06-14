s = input()
ans = []
for i in range(len(s)):
    if '0'<=s[i]<='9':
        ans.append(s[i])

print(''.join(ans))