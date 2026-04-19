class Solution:
    def mergeAlternately(self, word1, word2):
        result = []
        i = 0

        # Step 1: alternate
        while i < len(word1) and i < len(word2):
            result.append(word1[i])
            result.append(word2[i])
            i += 1

        # Step 2: leftovers
        result.append(word1[i:])
        result.append(word2[i:])

        return "".join(result)

# word1 = input().strip('"')
# word2 = input().strip('"')
# obj = Solution()
# print(obj.mergeAlternately(word1, word2))



class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        i=0
        final_gcd = []

        while i < len(str1) and i <len(str2):
            
            print(final_gcd)
            if len(str1) < len(str2):
                if str1[i] == str2[i]:
                    if str1[i] not in final_gcd:
                        final_gcd.append(str1[i])
            elif len(str2) < len(str1):
                if str2[i] == str1[i]:
                    if str2[i] not in final_gcd:
                        final_gcd.append(str2[i])

            print(final_gcd)

            i=i+1

        return ''.join(final_gcd)

str1 = input().strip('"')
str2 = input().strip('"')
obj = Solution()
print(obj.gcdOfStrings(str1, str2))