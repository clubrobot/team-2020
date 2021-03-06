#ifndef __SERIALTALKS_H__
#define __SERIALTALKS_H__

#include <Arduino.h>
#include "serialutils.h"
#include "CRC16.h"
#include "thread_tools.h"

#ifndef EEPROM_SIZE
#define EEPROM_SIZE 512
#endif

#ifndef SERIALTALKS_BAUDRATE
#define SERIALTALKS_BAUDRATE 115200
#endif

#ifndef SERIALTALKS_INPUT_BUFFER_SIZE
#define SERIALTALKS_INPUT_BUFFER_SIZE 64
#endif

#ifndef SERIALTALKS_OUTPUT_BUFFER_SIZE
#define SERIALTALKS_OUTPUT_BUFFER_SIZE 64
#endif

#ifndef SERIALTALKS_UUID_ADDRESS
#define SERIALTALKS_UUID_ADDRESS 0x0000000000
#endif

#ifndef SERIALTALKS_UUID_LENGTH
#define SERIALTALKS_UUID_LENGTH 32
#endif

#ifndef SERIALTALKS_MAX_PROCESSING
#define SERIALTALKS_MAX_PROCESSING 0x4
#endif

#ifndef SERIALTALKS_MAX_OPCODE
#define SERIALTALKS_MAX_OPCODE 0x20
#endif

#define SERIALTALKS_MASTER_BYTE 'R'
#define SERIALTALKS_SLAVE_BYTE 'A'

#define SERIALTALKS_DEFAULT_UUID_LENGTH 9

#define SERIALTALKS_RESEVED_OPCODE_0 0X0
#define SERIALTALKS_RESEVED_OPCODE_1 0X1
#define SERIALTALKS_RESEVED_OPCODE_2 0X2
#define SERIALTALKS_RESEVED_OPCODE_3 0X3
#define SERIALTALKS_RESEVED_OPCODE_4 0X4
#define SERIALTALKS_RESEVED_OPCODE_5 0X5
#define SERIALTALKS_RESEVED_OPCODE_6 0X6
#define SERIALTALKS_RESEVED_OPCODE_7 0X7
#define SERIALTALKS_RESEVED_OPCODE_8 0X8
#define SERIALTALKS_RESEVED_OPCODE_9 0X9

#define SERIALTALKS_PING_OPCODE (SERIALTALKS_RESEVED_OPCODE_0)
#define SERIALTALKS_GETUUID_OPCODE (SERIALTALKS_RESEVED_OPCODE_1)
#define SERIALTALKS_SETUUID_OPCODE (SERIALTALKS_RESEVED_OPCODE_2)
#define SERIALTALKS_DISCONNECT_OPCODE (SERIALTALKS_RESEVED_OPCODE_3)
#define SERIALTALKS_GETEEPROM_OPCODE (SERIALTALKS_RESEVED_OPCODE_4)
#define SERIALTALKS_SETEEPROM_OPCODE (SERIALTALKS_RESEVED_OPCODE_5)
#define SERIALTALKS_GETBUFFERSIZE_OPCODE (SERIALTALKS_RESEVED_OPCODE_6)
#define SERIALTALKS_RESEND_OPCODE 0xFE
#define SERIALTALKS_FREE_BUFFER_OPCODE 0xFA
#define SERIALTALKS_STDOUT_RETCODE 0xFFFFFFFF
#define SERIALTALKS_STDERR_RETCODE 0xFFFFFFFE

#define SERIALTALKS_CRC_SIZE 2

class SerialTalks
{
public: // Public API
    class ostream : public Print
    {
    public:
        virtual size_t write(uint8_t);
        virtual size_t write(const uint8_t *buffer, size_t size);

        template <typename T>
        ostream &operator<<(const T &object)
        {
            print(object);
            return *this;
        }

    protected:
        void begin(SerialTalks &parent, long retcode);

        SerialTalks *m_parent;
        long m_retcode;

        friend class SerialTalks;
    };

    typedef void (*Instruction)(SerialTalks &inst, Deserializer &input, Serializer &output);
    typedef void (*Processing)(SerialTalks &inst, Deserializer &input);

    void begin(Stream &stream);

    void bind(byte opcode, Instruction instruction);
    void attach(byte opcode, Processing processing);

    bool execinstruction(byte *inputBuffer);
    bool execute();

    Serializer getSerializer() { return Serializer(m_outputBuffer); }
    int send(byte opcode, Serializer output);

    bool isConnected() const { return m_connected; }

    bool waitUntilConnected(float timeout = -1);

    bool getUUID(char *uuid);
    void setUUID(const char *uuid);

    static void generateRandomUUID(char *uuid, int length);

    // Public attributes (yes we dare!)

    ostream out;
    ostream err;

protected: // Protected methods
    int sendback(long retcode, const byte *buffer, int size);

    bool receive(byte *inputBuffer);

    // Attributes

    Stream *m_stream;
    bool m_connected;

    Instruction m_instructions[SERIALTALKS_MAX_OPCODE];
    Processing m_processings[SERIALTALKS_MAX_PROCESSING];

    byte m_inputBuffer[SERIALTALKS_INPUT_BUFFER_SIZE];
    byte m_outputBuffer[SERIALTALKS_OUTPUT_BUFFER_SIZE];

    enum //     m_state
    {
        SERIALTALKS_WAITING_STATE,
        SERIALTALKS_INSTRUCTION_STARTING_STATE,
        SERIALTALKS_CRC_RECIEVING_STATE,
        SERIALTALKS_INSTRUCTION_RECEIVING_STATE,
    } m_state;

    enum // m_order
    {
        SERIALTALKS_ORDER,
        SERIALTALKS_RETURN,
    } m_order;

    byte m_bytesNumber;
    byte m_bytesCounter;
    long m_lastTime;
    unsigned long m_lastRetcode;

    // for cyclic redundancy check
    CRC16 m_crc;

    byte m_crcBytesCounter;
    uint16_t received_crc_value;

    byte m_crc_tab[SERIALTALKS_CRC_SIZE + 1];
    byte m_crc_tmp[SERIALTALKS_OUTPUT_BUFFER_SIZE];

    Mutex m_mutex; //send mutex

private:
    void launchResend(void);
    void freeBuffer(void);

    static void PING(SerialTalks &talks, Deserializer &input, Serializer &output);
    static void GETUUID(SerialTalks &talks, Deserializer &input, Serializer &output);
    static void SETUUID(SerialTalks &talks, Deserializer &input, Serializer &output);
    static void DISCONNECT(SerialTalks &talks, Deserializer &input, Serializer &output) { ESP.restart(); }
    static void GETEEPROM(SerialTalks &talks, Deserializer &input, Serializer &output);
    static void SETEEPROM(SerialTalks &talks, Deserializer &input, Serializer &output);
    static void GETBUFFERSIZE(SerialTalks &talks, Deserializer &input, Serializer &output);
};

extern SerialTalks talks;

#endif // __SERIALTALKS_H__
