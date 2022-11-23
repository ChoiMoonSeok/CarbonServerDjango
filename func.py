# 조직 구조를 반환하는 함수
def put_struct(result, Company):
    if Company['upper'] == None:
        result['Children'].append(Company)
        return 0
    elif result['depth'] == Company['depth'] - 1:
        if result['id'] == Company['upper']:
            result['Children'].append(Company)
        else:
            return 0
    else:
        if len(result['Children']) != 0:
            for i in range(len(result['Children'])):
                temp = result['Children'][i]
                put_struct(temp, Company)
        else:
            if result['id'] == Company['upper']:
                result['Children'].append(Company)
            else:
                return 0