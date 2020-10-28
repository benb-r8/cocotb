import logging

import cocotb
from cocotb.binary import BinaryValue
from cocotb.triggers import Timer
from cocotb.result import TestFailure
from cocotb.handle import Force, Release


@cocotb.test(expect_fail=cocotb.SIM_NAME in ["GHDL"])
async def force_release(dut):
    """
    Test force and release on simulation handles
    """
    log = logging.getLogger("cocotb.test")
    await Timer(10, "ns")

    fail = []

    log.info("forcing logic value")
    dut.stream_out_ready <= 1
    dut.stream_in_ready <= Force(0)
    await Timer(10, "ns")
    got_in = int(dut.stream_out_ready)
    got_out = int(dut.stream_in_ready)
    log.info("dut.stream_out_ready = %d", got_in)
    log.info("dut.stream_in_ready = %d", got_out)
    if got_in == got_out:
        fail.append("stream_out_ready and stream_in_ready should not match when force is active!")
    dut.stream_in_ready <= Release()
    await Timer(10, "ns")

    log.info("forcing logic value vector")
    dut.stream_in_data <= 4
    dut.stream_out_data_comb <= Force(5)
    await Timer(10, "ns")
    got_in = int(dut.stream_in_data)
    got_out = int(dut.stream_out_data_comb)
    log.info("dut.stream_in_data = %d", got_in)
    log.info("dut.stream_out_data_comb = %d", got_out)
    if got_in == got_out:
        fail.append("stream_in_data and stream_out_data_comb should not match when force is active!")
    await Timer(10, "ns")

    log.info("releasing logic value vector")
    dut.stream_out_data_comb <= Release()
    dut.stream_in_data <= 3
    await Timer(10, "ns")
    got_in = int(dut.stream_in_data)
    got_out = int(dut.stream_out_data_comb)
    log.info("dut.stream_in_data = %d", got_in)
    log.info("dut.stream_out_data_comb = %d", got_out)
    if got_in != got_out:
        fail.append("stream_in_data and stream_out_data_comb should match when output was released!")

    log.info("forcing integer")
    dut.stream_in_int <= 4
    dut.stream_out_int <= Force(5)
    await Timer(10, "ns")
    got_in = int(dut.stream_in_int)
    got_out = int(dut.stream_out_int)
    log.info("dut.stream_in_int = %d", got_in)
    log.info("dut.stream_out_int = %d", got_out)
    if got_in == got_out:
        fail.append("stream_in_int and stream_out_int should not match when force is active!")
    dut.stream_in_ready <= Release()
    await Timer(10, "ns")

    log.info("forcing bool")
    dut.stream_in_bool <= 1
    dut.stream_out_bool <= Force(0)
    await Timer(10, "ns")
    got_in = int(dut.stream_in_bool)
    got_out = int(dut.stream_out_bool)
    log.info("dut.stream_in_bool = %d", got_in)
    log.info("dut.stream_out_bool = %d", got_out)
    if got_in == got_out:
        fail.append("stream_in_bool and stream_out_bool should not match when force is active!")
    dut.stream_in_ready <= Release()
    await Timer(10, "ns")

    log.info("forcing wide logic vector")
    binval_in = BinaryValue(bytes.fromhex("0000000000000008"))
    binval_force = BinaryValue(bytes.fromhex("0000000000000004"))
    dut.stream_in_data_wide <= binval_in
    dut.stream_out_data_wide <= Force(binval_force)
    await Timer(10, "ns")
    got_in = dut.stream_in_data_wide.value.buff
    got_out = dut.stream_out_data_wide.value.buff
    log.info("dut.stream_in_data_wide = 0x%s", got_in.hex())
    log.info("dut.stream_out_data_wide = 0x%s", got_out.hex())
    if got_in == got_out:
        fail.append("stream_in_data_wide and stream_out_data_wide should not match when force is active!")
    dut.stream_out_data_wide <= Release()
    await Timer(10, "ns")

    if fail:
        for f in fail:
            log.error(f)
        raise TestFailure("Encountered test failures.")