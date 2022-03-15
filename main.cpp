#include <iostream>
#include <Windows.h>
#include<Mmsystem.h>
#pragma comment(lib,"winmm.lib")
#include <chrono>
#include <string>
#include <fstream>
#include <winnt.h>
#include <iomanip>


char size_command1[20] = "mode con cols=";
char size_command2[20] = " lines=";

char* size_command3;
char* size_command4;
char* size_command;


using namespace std;

void cls(){
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    COORD coordScreen = { 0, 0 };
    SetConsoleCursorPosition( hConsole, coordScreen );
}

int main(){
    system("color 0f");
    CONSOLE_CURSOR_INFO cursor_info = {1, 0};
    SetConsoleCursorInfo(GetStdHandle(STD_OUTPUT_HANDLE), &cursor_info);

    ifstream codes_result;

    string sourse_w;
    string sourse_h;
    string frames;
    string ftime;

    codes_result.open("result.txt", ios::in);
    getline(codes_result, sourse_w);
    getline(codes_result, sourse_h);
    getline(codes_result, frames);
    getline(codes_result, ftime);
    const char* w = sourse_w.c_str();
    const char* h = sourse_h.c_str();
    int h_value = stoi(sourse_h);

    size_command3 = strcat(size_command1, w);
    size_command4 = strcat(size_command2, h);
    size_command = strcat(size_command3, size_command4);

    cout << size_command << endl;

    system(size_command);
    int frame = stoi(frames);
    int ft = stoi(ftime);
    double fti = double(ft) * 1000000000/ frame; //µ¥Ö¡Ê±¼ä
    string codes;
    int i = 0;
    int frame_use = 0;
    auto start = chrono::high_resolution_clock::now();
    auto end = chrono::high_resolution_clock::now();
    long long diff = 0;
    char *frame_codes = "";
    PlaySound(TEXT(TEXT("audio.wav")),NULL,SND_FILENAME | SND_ASYNC);
    while (getline(codes_result, codes)){
        diff = 0;
        cout << codes << endl;
        i++;
        if (i == h_value-1){
            frame_use++;
            cout << right << setw(5) << frame_use << '/' << frame << "  ";
            i = 0;
            while (diff < fti*frame_use){
                end = chrono::high_resolution_clock::now();
                diff = ((end - start).count());
            }
            cout << setw(10) << left << (diff)/1000000000.0 << '/';
            cout << setw(10) << left << fti*frame_use/1000000000.0  << "  ";
            cout << frame/ft << "fps";
            cls();
        }
    }

    cout << "END" << endl;
    getchar();
    return 0;

    /*start = chrono::high_resolution_clock::now();
    Sleep(1000);
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double, ratio<1, 1>> diff = end - start;
    cout << diff.count()*1000 << endl;*/

}