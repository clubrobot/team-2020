#include "SerialTopics.h"
#include "Clock.h"

// Global instance

SerialTopics topics;

void SerialTopics::START_SUBSCRIPTION(SerialTalks &talks, Deserializer &input, Serializer &output)
{
    byte opcode = input.read<byte>();
    long timestep = input.read<long>();

    if (opcode < SERIALTOPICS_MAX_OPCODE)
    {
        topics.getSubscriptions()[opcode].timestep = timestep;
        topics.getSubscriptions()[opcode].lasttime = 0;
        topics.getSubscriptions()[opcode].enable = true;
        output.write<bool>(true);
    }
    else
    {
        output.write<bool>(false);
    }
}

void SerialTopics::STOP_SUBSCRIPTION(SerialTalks &talks, Deserializer &input, Serializer &output)
{
    byte opcode = input.read<byte>();

    if (opcode < SERIALTOPICS_MAX_OPCODE)
    {
        topics.getSubscriptions()[opcode].enable = false;
        output.write<bool>(true);
    }
    else
    {
        output.write<bool>(false);
    }
}

void SerialTopics::GET_SUBSCRIPTION_STATE(SerialTalks &talks, Deserializer &input, Serializer &output)
{
    byte opcode = input.read<byte>();

    if (opcode < SERIALTOPICS_MAX_OPCODE)
    {
        output.write<long>(topics.getSubscriptions()[opcode].timestep);
        output.write<bool>(topics.getSubscriptions()[opcode].enable);
    }
    else
    {
        output.write<long>(-1);
        output.write<bool>(false);
    }
}

void SerialTopics::DEFAULT_HANDLER(Serializer &output)
{
}

void SerialTopics::begin(SerialTalks &talks)
{
    _talks = &talks;

    _talks->bind(START_SUBSCRIPTION_OPCODE, START_SUBSCRIPTION);
    _talks->bind(STOP_SUBSCRIPTION_OPCODE, STOP_SUBSCRIPTION);
    _talks->bind(GET_SUBSCRIPTION_STATE_OPCODE, GET_SUBSCRIPTION_STATE);

    for (int i = 0; i < SERIALTOPICS_MAX_OPCODE; i++)
    {
        _subscriptions[i].timestep = SERIALTOPICS_DEFAULT_TIMING;
        _subscriptions[i].enable = false;
        _subscriptions[i].func = DEFAULT_HANDLER;
    }
}

void SerialTopics::bind(byte opcode, Subscription subscription)
{
    if (opcode < SERIALTOPICS_MAX_OPCODE)
        _subscriptions[opcode].func = subscription;
}

bool SerialTopics::execute()
{
    long currentTime = millis();
    for (int i = 0; i < SERIALTOPICS_MAX_OPCODE; i++)
    {
        if (_subscriptions[i].enable && currentTime - _subscriptions[i].lasttime > _subscriptions[i].timestep)
        {
            Serializer ser = _talks->getSerializer();
            _subscriptions[i].func(ser);
            _talks->send(i, ser);
            _subscriptions[i].lasttime = currentTime;
        }
    }
    return true;
}