import {useState, useCallback} from 'react';

function InputValue(field) {
    let [value, setValue] = useState('');
    let [error, setError] = useState('');

    let onChange = useCallback(function (event) {
        setValue(event.currentTarget.value);
        setError('');
    }, []);

    let parseServerError = errors => {
        if (errors && errors[field]) {
            setError(errors[field][0]);
        }
    };

    return {
        value,
        setValue,
        reset: () => setValue(''),
        bind: {
            value,
            onChange
        },
        error,
        setError,
        parseServerError
    };
}

export default InputValue;
