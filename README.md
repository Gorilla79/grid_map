# grid_map

SLAM을 통해 생성한 맵을 Path Planning에 사용하기 위해 이미지 처리를 하는 과정

사용한 map데이터는 result.png을 사용하였으며
![result](https://github.com/user-attachments/assets/9572a8ca-3df3-480a-b80d-9e87cc54fba4)

---

1. 이미지 색상 변경<br/>
![image](https://github.com/user-attachments/assets/1cd833a1-acc1-48de-867b-22ae712fc9f5)

2. 그리드화<br/>
[그리드 영역 10일때]
![image](https://github.com/user-attachments/assets/58486abf-be6a-4cca-adff-c795dba7619e)

[그리드 영역 1일때]
![image](https://github.com/user-attachments/assets/df4fe345-502c-4cd8-ad94-9f8352235a3c)

3. 0과 1의 탐색 구역 생성
![image](https://github.com/user-attachments/assets/37b60beb-1343-4c34-8809-6cee9fcec9a0)

정상동작은 모두 가능!<br/> 
##[가장 잘 동작하는 코드] <br/> 
change png.py / grid_map_test2(very).py / grid_map_binary.py[가장 최종]
